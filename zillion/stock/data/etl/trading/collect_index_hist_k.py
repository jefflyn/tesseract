import tushare as ts

from zillion.future.db_util import get_db
from zillion.stock.data.data_util import INDEX_DICT
from zillion.utils import date_util


def collect_index_hist_k(start=None):
    '''
    获取指数历史行情
    :param start:
    :return:
    '''
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    start_trade_date = date_util.get_latest_trade_date()[0] if start is None else start

    # index_code = list(INDEX_DICT.keys())[0]
    # check_sql = "select 1 from index_hist_k where code='" + index_code + "' and trade_date='" + str(
    #     start_trade_date) + "'"
    # total = cursor.execute(check_sql)
    # if total > 0:
    #     print(start_trade_date + " index data existed")
    #     # sys.exit(0)
    for code in INDEX_DICT.keys():
        index_k = ts.get_k_data(code=code, start=start_trade_date, ktype='D', autype='qfq', index=True)
        if index_k.empty is True or index_k is None:
            print(code, start_trade_date, 'no index data found, continue...')
            continue
        index_k.index = index_k['date']
        for index, row in index_k.iterrows():
            trade_date = row['date']
            pre_trade_date = date_util.get_previous_trade_day(trade_date)
            pre_trade_index = index_k[index_k.date == pre_trade_date]
            if pre_trade_index.empty is True or pre_trade_index is None:
                # print(pre_trade_date, code, 'no index data found, retry...')
                pre_trade_index = ts.get_k_data(code=code, start=pre_trade_date, end=pre_trade_date,
                                        ktype='D', autype='qfq', index=True)
            if pre_trade_index.empty is True:
                print(code, pre_trade_date, 'no pre-date index data found, continue...')
                continue
            pre_close = float(pre_trade_index.loc[pre_trade_index.index[0], 'close'])
            close = float(row['close'])
            pct_change = round((close - pre_close) / pre_close * 100, 2)
            curt_values = (trade_date, code, row['open'], close, row['high'], row['low'], row['volume'], pct_change)
            insert_values = [curt_values]

            try:
                # 注意这里使用的是executemany而不是execute
                insert_count = cursor.executemany(
                    'insert into index_hist_k(trade_date,code,open,close,high,low,volume,pct_change)'
                    'values(%s,%s,%s,%s,%s,%s,%s,%s)', insert_values)
                db.commit()
                print(code, trade_date, 'index data insert successfully.')
            except Exception as err:
                print('>>> failed!', err)
                db.rollback()

    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    collect_index_hist_k(start='2020-05-06')

