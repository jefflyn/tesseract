from stocks.base.pro_util import pro
from stocks.base.logging import logger
from stocks.data import _datautils
import datetime
import time
import pymysql

if __name__ == '__main__':
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20100101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    # 建立数据库连接,剔除已入库的部分
    db = pymysql.connect(host='127.0.0.1', user='linjingu', passwd='linjingu', db='stocks', charset='utf8')
    cursor = db.cursor()
    # 设定需要获取数据的股票池
    # stock_pool = ['600069.SH', '002895.SZ', '002923.SZ', '000820.SZ', '002555.SZ']
    total = cursor.execute("select ts_code from stock_basic")
    if total == 0:
        logger.info("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    call_time = 0
    for i in range(len(stock_pool)):
        try:
            # 睡1分钟
            # if call_time == 200:
            #     call_time = 0
            #     logger.info('process is sleeping for 1 minute ...')
            #     time.sleep(30)

            df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
            # 打印进度
            logger.info('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
            call_time += 1
        except Exception as aa:
            logger.info(aa)
            logger.info('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.ix[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO stock_hist_day(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                    state_dt, str(resu[0]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]),
                    float(resu[9]),
                    float(resu[10]), float(resu[6]), float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                logger.error(err)
                continue
    cursor.close()
    db.close()
    logger.info('All Finished!')
