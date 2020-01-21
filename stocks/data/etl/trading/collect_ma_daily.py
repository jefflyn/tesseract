import datetime
import time
import numpy as np
import tushare as ts
from stocks.util.db_util import get_db
from stocks.util.pro_util import pro
from stocks.gene import maup

import stocks.util.display

if __name__ == '__main__':
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    time_temp = datetime.datetime.now() - datetime.timedelta(days=365*2)
    start_dt = time_temp.strftime('%Y%m%d')
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    ma = [5, 10, 20, 30, 60, 90, 120, 250]
    print("Collect ma data from " + start_dt + " to " + end_dt)

    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    total = cursor.execute("select ts_code from basic")
    if total == 0:
        print("no stock basic found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    cursor.execute("delete from hist_ma_day")
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    for i in range(len(stock_pool)):
        try:
            # 打印进度
            if i % 200 == 0:
                print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            # 前复权行情
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], adj='qfq', ma=ma, start_date=start_dt, end_date=end_dt)
            if df is None:
                continue
        except Exception as e:
            print(e)
            print('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=stock_pool[i], adj='qfq', ma=ma, start_date=start_dt, end_date=end_dt)
            # 打印进度
            print('redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))

        df = df.head(1)
        cols = df.columns
        c_len = df.shape[0]
        for j in range(c_len):
            resu0 = list(df.iloc[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            trade_date = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                code = str(resu[0][0:6])
                price = float(resu[5])
                ma5 = float(resu[11])
                ma10 = float(resu[13])
                ma20 = float(resu[15])
                ma30 = float(resu[17])
                ma60 = float(resu[19])
                ma90 = float(resu[21])
                ma120 = float(resu[23])
                ma250 = float(resu[25])
                ma_arr = [price, ma5, ma10, ma20, ma30, ma60, ma90, ma120, ma250]
                ma_arr = np.round(ma_arr, 2)
                # np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
                grade = maup.get_ma_point(ma_arr)

                sql_insert = "INSERT INTO hist_ma_day(code,trade_date,grade,price,ma5,ma10,ma20,ma30,ma60,ma90,ma120,ma250) " \
                             "VALUES ('%s', '%s', '%.1f', '%.2f', '%.2f', '%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f')" % (
                                 code, trade_date, grade, price, ma5, ma10, ma20, ma30, ma60, ma90, ma120, ma250)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                continue
    cursor.close()
    db.close()
    print('All Finished!')
