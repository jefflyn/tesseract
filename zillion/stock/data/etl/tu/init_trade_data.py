import datetime
import time

import tushare as ts
from zillion.utils.pro_util import pro

from zillion.stock.data import data_util
from zillion.utils import date_util
from zillion.utils.db_util import get_db

INIT_DATA = True
INIT_DATA_START_DATE = '20100101'


def init_hist_daily(codes=[]):
    """
    收集日交易数据，前复权
    """
    start_time = datetime.datetime.now()
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    start_dt = INIT_DATA_START_DATE
    end_dt = date_util.get_today(date_util.FORMAT_FLAT)
    print('Collect trade data from ', start_dt, ' to ', end_dt, ', @', start_time)

    # get_code_sql = 'select ts_code from basics '
    # if len(codes) > 0:
    #     code_str = ','.join(str(n) for n in codes)
    #     get_code_sql = get_code_sql + 'where code in (' + code_str + ')'
    # total = cursor.execute(get_code_sql)
    total = len(codes)
    if total == 0:
        print('no stock found, process end!')
        exit(0)
    # stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    stock_pool = codes
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    begin_time = datetime.datetime.now()
    for i in range(len(stock_pool)):
        ts_code = str(stock_pool[i])
        code = ts_code[0:6]
        try:
            # 打印进度
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + ts_code)
            if i > 0 and i % 198 == 0:
                end_time = datetime.datetime.now()
                time_diff = (end_time - begin_time).seconds
                sleep_time = 60 - time_diff
                if sleep_time > 0:
                    print('sleep for ' + str(sleep_time) + ' seconds ...')
                    time.sleep(sleep_time)
                begin_time = datetime.datetime.now()
            # 前复权行情
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=start_dt, end_date=end_dt)
        except Exception as e:
            # print(e)
            print('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=start_dt, end_date=end_dt)
            # 打印进度
            print('Redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + ts_code)
        if df is None:
            continue
        df['trade_date'] = df['trade_date'].apply(lambda x: date_util.parse_date_str(str(x)))
        df['change'] = df['change'].apply(lambda x: round(float(x), 2))
        df['pre_close'] = df['pre_close'].apply(lambda x: round(float(x), 2))
        df['open'] = df['open'].apply(lambda x: round(float(x), 2))
        df['close'] = df['close'].apply(lambda x: round(float(x), 2))
        df['high'] = df['high'].apply(lambda x: round(float(x), 2))
        df['low'] = df['low'].apply(lambda x: round(float(x), 2))

        df['code'] = code
        insert_hist_list = df[['trade_date', 'ts_code', 'code', 'pre_close', 'open', 'close', 'high', 'low', 'vol',
                               'amount', 'change', 'pct_chg']].values.tolist()
        # print(insert_hist_list)
        try:
            cursor.execute("delete from hist_trade_day where ts_code='" + ts_code + "'")
            # 注意这里使用的是executemany而不是execute
            insert_count = cursor.executemany(
                'insert into hist_trade_day(trade_date, ts_code, code, pre_close, open, close, high, low, vol, amount, '
                'amt_change, pct_change)'
                'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', insert_hist_list)
            db.commit()
        except Exception as err:
            print('>>> insert data failed!', err)
            db.rollback()
    cursor.close()
    db.close()
    end_time = date_util.now()
    print('Init hist trade data finished! Consume time %d secs! Result size: %d\n' %
          ((end_time - start_time).seconds, total))


if __name__ == '__main__':
    # sql = 'select ts_code from basics where name like :dr_name or name like :xd_name or name like :xr_name '
    # df = data_util.read_sql(sql, params={"dr_name": "DR%", "xd_name": "XD%", "xr_name": "XR%"})

    # sql = 'select ts_code from basics where code like :sh_code'
    # df = data_util.read_sql(sql, params={"sh_code": "6%"})

    sql = 'select ts_code from basics where code like :sz_code'
    df = data_util.read_sql(sql, params={"sz_code": "0%"})

    # sql = 'select ts_code from basics where code like :cyb_code'
    # df = data_util.read_sql(sql, params={"cyb_code": "3%"})

    # all
    # sql = 'select ts_code from basics'
    # df = data_util.read_query(sql)

    init_codes = list(df['ts_code'])
    # init_codes = ['000700.SZ', '600513.SH']

    init_hist_daily(init_codes)
