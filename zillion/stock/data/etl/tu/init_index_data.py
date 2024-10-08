import datetime
import sys
import time

import tushare as ts
from zillion.utils.pro_util import pro

from zillion.stock.data.data_util import INDEX_LIST
from zillion.utils import date_util
from zillion.utils.db_util import get_db

if __name__ == '__main__':
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    index_code = INDEX_LIST[0]
    last_trade_date = date_util.get_latest_trade_date()[0]
    check_sql = "select 1 from hist_index_day where ts_code='" + index_code + "' and trade_date='" + str(last_trade_date) + "'"
    total = cursor.execute(check_sql)
    if total > 0:
        print(last_trade_date + " trade data existed")
        sys.exit(0)
    last_trade_date = date_util.get_latest_trade_date()[0]
    df = ts.pro_bar(api=pro, ts_code=index_code, asset='I', start_date=last_trade_date, end_date=last_trade_date)
    c_len = df.shape[0]
    if c_len == 0:  # 没有记录退出
        print(last_trade_date + " no index data found yet")
        sys.exit(0)

    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    time_temp = datetime.datetime.now() - datetime.timedelta(days=2)
    # start_dt = time_temp.strftime('%Y%m%d')
    start_dt = '20150101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    print("Collect index data from " + start_dt + " to " + end_dt)
    total = len(INDEX_LIST)
    stock_pool = INDEX_LIST
    # 循环获取指数日线行情
    # 1分钟不超过200次调用
    for i in range(len(stock_pool)):
        try:
            # 打印进度
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            # 前复权行情
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], asset='I', start_date=start_dt, end_date=end_dt)
            c_len = df.shape[0]
        except Exception as e:
            print('Exception: ' + str(e))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], asset='I', start_date=start_dt, end_date=end_dt)
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
                sql_insert = "INSERT INTO hist_index_day(trade_date, ts_code, code, pre_close, open, close, " \
                             "high, low, vol, amount, amt_change, pct_change) " \
                             "VALUES ('%s', '%s', '%s', '%.4f', '%.4f', '%.4f','%.4f','%.4f','%i','%.4f','%.4f','%.4f')" % (
                                 trade_date, str(resu[0]), str(resu[0])[0:6], float(resu[6]), float(resu[3]), float(resu[2]),
                                 float(resu[4]), float(resu[5]), float(resu[9]), float(resu[10]), float(resu[7]), float(resu[8]))
                print(sql_insert)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                continue
    cursor.close()
    db.close()
    print('All Finished!')
