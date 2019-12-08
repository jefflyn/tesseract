from stocks.util import display

import datetime
import time
import sys
import random
import tushare as ts
from stocks.util.db_util import get_db
from stocks.util.logging import logger
from stocks.util.pro_util import pro
from stocks.util import date_util


time_temp = datetime.datetime.now() - datetime.timedelta(days=3650)
start_dt = time_temp.strftime('%Y%m%d')
time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
end_dt = time_temp.strftime('%Y%m%d')


def collect_weekly():
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()

    random_stocks = ['600000.SH', '600016.SH', '601988.SH', '600019.SH', '600028.SH', '600029.SH',
                     '600030.SH', '600036.SH', '600048.SH', '600519.SH']
    current = random.randint(0, 9)
    last_trade_date = date_util.get_latest_trade_date(format=date_util.default_format)[0]
    check_sql = "select 1 from hist_weekly where ts_code='" + random_stocks[current] \
                + "' and trade_date='" + str(last_trade_date) + "'"
    total = cursor.execute(check_sql)
    if total > 0:
        logger.info(last_trade_date + " trade data existed")
        # sys.exit(0)
    last_trade_date = date_util.get_latest_trade_date(format=date_util.format_flat)[0]
    df = pro.weekly(ts_code=random_stocks[current], adj='qfq', start_date=last_trade_date, end_date=last_trade_date)
    c_len = df.shape[0]
    if c_len == 0:
        logger.info(last_trade_date + " no trade data found yet")
        # sys.exit(0)
    total = cursor.execute('select ts_code from basic')
    if total == 0:
        logger.info("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    logger.info("Collect trade data from " + start_dt + " to " + end_dt)
    # 1分钟不超过200次调用
    begin_time = date_util.get_now()
    for i in range(len(stock_pool)):
        try:
            # 打印进度
            logger.debug('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            # 每分钟最多访问该接口120次
            if i > 0 and i % 120 == 0:
                end_time = date_util.get_now()
                time_diff = (end_time - begin_time).seconds
                sleep_time = 63 - time_diff
                if sleep_time > 0:
                    logger.info('sleep for ' + str(sleep_time) + ' seconds ...')
                    time.sleep(sleep_time)
                begin_time = datetime.datetime.now()
            # 前复权行情
            df = pro.weekly(ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            if df is None:
                continue
            c_len = df.shape[0]
        except Exception as e:
            # print(e)
            logger.debug('No DATA Code: ' + str(i))
            time.sleep(60)
            df = pro.weekly(api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            # 打印进度
            logger.debug('Redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
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
                sql_insert = "INSERT INTO hist_weekly(trade_date,ts_code,code,pre_close,open,close,high,low,vol,amount,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%.2f','%i','%.4f','%.2f','%.4f')" % (
                                 trade_date, str(resu[0]), str(resu[0])[0:6], float(resu[6]), float(resu[2]),
                                 float(resu[5]), float(resu[3]), float(resu[4]),
                                 float(resu[9]), float(resu[10]), float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                logger.error(err)
                continue
    cursor.close()
    db.close()
    logger.info('All Finished!')


if __name__ == '__main__':
    collect_weekly()
    # df = pro.weekly(ts_code='300123.SZ', adj='hfq', start_date=start_dt, end_date=end_dt)
    # print(df)
    # histdf = ts.get_hist_data(code='300123', ktype='W', start='2019-04-30')
    # print(histdf)
