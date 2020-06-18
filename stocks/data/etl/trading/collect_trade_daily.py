import datetime
import time

import tushare as ts

from stocks.util import date_util
from stocks.util.db_util import get_db
from stocks.util.pro_util import pro

INIT_DATA_START_DATE = '20100101'


if __name__ == '__main__':
    """
    收集日交易数据，前复权
    """
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    start_dt = date_util.shift_date(type='d', n=-2, format='YYYYMMDD')
    # start_dt = date_util.shift_date(type='d', n=-7, format='YYYYMMDD')

    end_dt = date_util.get_today(date_util.FORMAT_FLAT)
    print("Collect trade data from " + start_dt + " to " + end_dt)

    total = cursor.execute('select ts_code, name from basics')
    if total == 0:
        print("no stock found, process end!")
        exit(0)
    # a = cursor.fetchall()
    stock_pool = [ts_code_tuple for ts_code_tuple in cursor.fetchall()]
    # stock_pool = ['002414.SZ']
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    begin_time = datetime.datetime.now()
    for i in range(len(stock_pool)):
        act_start_date = start_dt
        ts_code = stock_pool[i][0]
        name = stock_pool[i][1]
        init_flat = ['DR', 'XD', 'XR']
        need_init = name[0:2] in init_flat
        if need_init:
            print(str(stock_pool[i]), ' init hist trade data')
            act_start_date = INIT_DATA_START_DATE
            cursor.execute("delete from hist_trade_day where ts_code='" + ts_code + "'")
        try:
            # 打印进度
            if i % 200 == 0:
                print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            if i > 0 and i % 198 == 0:
                end_time = datetime.datetime.now()
                time_diff = (end_time - begin_time).seconds
                sleep_time = 60 - time_diff
                if sleep_time > 0:
                    print('sleep for ' + str(sleep_time) + ' seconds ...')
                    time.sleep(sleep_time)
                begin_time = datetime.datetime.now()
            # 前复权行情
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=act_start_date, end_date=end_dt)
            if df is None:
                continue
            c_len = df.shape[0]
        except Exception as e:
            # print(e)
            print('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=act_start_date, end_date=end_dt)
            # 打印进度
            print('Redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]

        for j in range(c_len):
            resu0 = list(df.loc[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            trade_date = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO hist_trade_day(trade_date, ts_code, code, pre_close, open, close, high, low, " \
                             "vol, amount, amt_change, pct_change) " \
                             "VALUES ('%s', '%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%.2f','%i','%.4f','%.2f','%.4f')" % (
                    trade_date, str(resu[0]), str(resu[0])[0:6], float(resu[6]), float(resu[2]), float(resu[5]),
                    float(resu[3]), float(resu[4]), float(resu[9]), float(resu[10]),  float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                db.rollback()
                continue
    cursor.close()
    db.close()
    print('All Finished!')
