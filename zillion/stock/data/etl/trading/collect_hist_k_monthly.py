import tushare as ts

from zillion.utils import date_util
from zillion.utils.db_util import get_db


def collect_monthly(start_time=None, end_time=None):
    if start_time is None:
        start_k_time = date_util.get_last_month_start()
    else:
        start_k_time = date_util.get_previous_month_trade_end(start_time)
    if end_time is None:
        end_time = date_util.get_this_month_end()
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()

    total = cursor.execute('select code from basics')
    if total == 0:
        print("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    print(date_util.now(), " Collect k data from " + start_k_time + " to " + end_time)

    for code in stock_pool:
        kdf = ts.get_k_data(code=code, start=start_k_time, end=end_time, ktype='M', autype='qfq', index=False)
        if kdf is None or kdf.empty:
            continue
        kdf = kdf.sort_values(by='date', ascending=False)
        kdf.index = kdf['date']
        insert_values = []
        for index, row in kdf.iterrows():
            code = str(row['code'])
            ts_code = code + '.SH' if code[0:1] == '6' else code + '.SZ'
            trade_date = row['date']
            pre_trade_date = date_util.get_previous_month_trade_end(trade_date)
            pre_k = kdf[kdf.date == pre_trade_date]
            if pre_k is None or pre_k.empty:
                # print(code, pre_trade_date, 'no pre-date k data found, continue...')
                continue

            pre_close = float(pre_k.loc[pre_k.index[0], 'close'])
            close = float(row['close'])
            pct_change = (close - pre_close) / pre_close * 100

            curt_values = (trade_date, ts_code, code, close, row['open'], row['high'], row['low'], round(pre_close, 2),
                           round(close - pre_close, 2), round(pct_change, 2), row['volume'], 0)
            insert_values.append(curt_values)

        try:
            del_sql = "delete from hist_monthly where code='" + code + "' and trade_date >= '" + start_time + "'"
            cursor.execute(del_sql)
            # 注意这里使用的是executemany而不是execute
            insert_count = cursor.executemany(
                'insert into hist_monthly(trade_date, ts_code, code, close, open, high, low, pre_close, '
                'amt_change, pct_change, volume, amount)'
                'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', insert_values)
            db.commit()
            print(code, trade_date, 'monthly k data insert successfully.')
        except Exception as err:
            print('>>> failed!', err)
            db.rollback()
    cursor.close()
    db.close()
    print(date_util.now(), ' All Finished!')


if __name__ == '__main__':
    collect_monthly(start_time='2021-01-01', end_time=None)

