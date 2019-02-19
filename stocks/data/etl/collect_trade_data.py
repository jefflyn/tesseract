import datetime
import time
import tushare as ts
from stocks.base.db_util import get_db
from stocks.base.logging import logger
from stocks.base.pro_util import pro

if __name__ == '__main__':
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    # start_dt = '20100101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=3)
    start_dt = time_temp.strftime('%Y%m%d')
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    logger.info("Collect trade data from " + start_dt + " to " + end_dt)
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    total = cursor.execute("select ts_code from basics")
    if total == 0:
        logger.info("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    # stock_pool = ['002923.SZ']
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    for i in range(len(stock_pool)):
        try:
            # 打印进度
            logger.info('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            # ts_code = stock_pool[i]
            # query_sql = "select ts_code from hist_trade_day where ts_code='{0}' and trade_date='{1}'"\
            #     .format(ts_code, time_temp.strftime('%Y-%m-%d'))
            # is_existed = cursor.execute(query_sql)
            # if is_existed > 0:
            #     continue
            # 前复权行情
            df = ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            if df is None:
                continue
            c_len = df.shape[0]
        except Exception as e:
            # print(e)
            logger.info('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            # 打印进度
            logger.info('redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        for j in range(c_len):
            resu0 = list(df.ix[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            trade_date = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO hist_trade_day(trade_date,ts_code,pre_close,open,close,high,low,vol,amount,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%.2f','%i','%.4f','%.2f','%.4f')" % (
                    trade_date, str(resu[0]), float(resu[6]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]),
                    float(resu[9]), float(resu[10]),  float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                logger.error(err)
                continue
    cursor.close()
    db.close()
    logger.info('All Finished!')
