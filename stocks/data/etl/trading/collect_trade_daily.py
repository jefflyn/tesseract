import datetime
import random
import time

import tushare as ts

from stocks.util import date_util
from stocks.util.db_util import get_db
from stocks.util.pro_util import pro

# 初始化数据True
INIT_DATA = False
INIT_DATA_START_DATE = '20150101'


if __name__ == '__main__':
    """
    收集日交易数据，前复权
    """
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()

    random_stocks = ['600000.SH', '600016.SH', '601988.SH', '600019.SH', '600028.SH', '600029.SH',
                     '600030.SH', '600036.SH', '600048.SH', '600519.SH']
    current = random.randint(0, 9)
    last_trade_date = date_util.get_latest_trade_date()[0]
    check_sql = "select 1 from hist_trade_day where ts_code='" + random_stocks[current] \
                + "' and trade_date='" + str(last_trade_date) + "'"
    total = cursor.execute(check_sql)
    if total > 0:
        print(last_trade_date + " trade data existed")
        # sys.exit(0)
    last_trade_date = date_util.get_latest_trade_date()[0].replace('-', '')
    df = ts.pro_bar(api=pro, ts_code=random_stocks[current], adj='qfq', start_date=last_trade_date, end_date=last_trade_date)
    c_len = df.shape[0]
    if c_len == 0:
        print(last_trade_date + " no trade data found yet")
        # sys.exit(0)
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    # time_temp = datetime.datetime.now() - datetime.timedelta(days=2)
    time_temp = datetime.datetime.now() - datetime.timedelta(days=10)

    start_dt = time_temp.strftime('%Y%m%d')
    if INIT_DATA:
        start_dt = INIT_DATA_START_DATE
        cursor.execute('truncate table hist_trade_day')
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    print("Collect trade data from " + start_dt + " to " + end_dt)

    total = cursor.execute('select ts_code from basics')
    if total == 0:
        print("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    # stock_pool = ['002414.SZ']
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    begin_time = datetime.datetime.now()
    for i in range(len(stock_pool)):
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
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            if df is None:
                continue
            c_len = df.shape[0]
        except Exception as e:
            # print(e)
            print('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
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
                sql_insert = "INSERT INTO hist_trade_day(trade_date,ts_code,code,pre_close,open,close,high,low,vol,amount,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%.2f','%i','%.4f','%.2f','%.4f')" % (
                    trade_date, str(resu[0]), str(resu[0])[0:6], float(resu[6]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]),
                    float(resu[9]), float(resu[10]),  float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                continue
    cursor.close()
    db.close()
    print('All Finished!')
