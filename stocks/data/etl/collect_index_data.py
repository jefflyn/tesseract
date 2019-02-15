import datetime
import time
import tushare as ts
from stocks.base.dbutils import get_db
from stocks.base.logging import logger
from stocks.base.pro_util import pro
from stocks.data.data_util import INDEX_LIST

if __name__ == '__main__':
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为当天
    # start_dt = '20100101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=3)
    start_dt = time_temp.strftime('%Y%m%d')
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    logger.info("Collect index data from " + start_dt + " to " + end_dt)
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    total = len(INDEX_LIST)
    stock_pool = INDEX_LIST
    # 循环获取指数日线行情
    # 1分钟不超过200次调用
    for i in range(len(stock_pool)):
        try:
            # 打印进度
            logger.info('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            # 前复权行情
            df = ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], asset='I', start_date=start_dt, end_date=end_dt)
            c_len = df.shape[0]
        except Exception as e:
            # print(e)
            logger.info('No DATA Code: ' + str(i))
            time.sleep(60)
            df = ts.pro_bar(pro_api=pro, ts_code=stock_pool[i], asset='I', start_date=start_dt, end_date=end_dt)
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
                sql_insert = "INSERT INTO hist_index_day(trade_date,ts_code,pre_close,open,close,high,low,vol,amount,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%.4f', '%.4f','%.4f','%.4f','%.4f','%i','%.4f','%.4f','%.4f')" % (
                                 trade_date, str(resu[0]), float(resu[6]), float(resu[2]), float(resu[5]),
                                 float(resu[3]), float(resu[4]),
                                 float(resu[9]), float(resu[10]), float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                logger.error(err)
                continue
    cursor.close()
    db.close()
    logger.info('All Finished!')
