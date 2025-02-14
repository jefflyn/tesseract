import datetime
import time

import tushare as ts
from zillion.utils.pro_util import pro

import zillion.stock.app.cn.service.hist_trade_service as hts
from utils.datetime import date_util
from zillion.utils.db_util import get_db

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

    # 获取上个交易日收盘价
    last_close_df = hts.get_last_close()
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    begin_time = datetime.datetime.now()
    for i in range(len(stock_pool)):
        ts_code = stock_pool[i][0]
        code = ts_code[0:6]
        exchange = ts_code[7:9]
        name = stock_pool[i][1]
        init_flat = ['DR', 'XD', 'XR']

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
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=start_dt, end_date=end_dt)
        except Exception as e:
            # print(e)
            print('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=start_dt, end_date=end_dt)
            # 打印进度
            print('Redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
        #无记录
        if df is None or df.empty:
            continue

        #是否需要初始化数据
        need_init = False
        is_big_gap = False
        if exchange == 'SZ':
            last_close_rd = last_close_df[last_close_df.code == code]
            if last_close_rd.empty is False:
                last_close = last_close_rd.loc[code, 'close']
                latest_close = df.loc[0, 'close']
                gap = abs(latest_close - last_close) / last_close * 100
                if gap > 11:
                    is_big_gap = True
        need_init = name[0:2] in init_flat or is_big_gap
        if need_init:
            print(str(stock_pool[i]), ' init hist trade data')
            cursor.execute("delete from hist_trade_day where ts_code='" + ts_code + "'")
            df = ts.pro_bar(api=pro, ts_code=ts_code, adj='qfq', start_date=INIT_DATA_START_DATE, end_date=end_dt)

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
