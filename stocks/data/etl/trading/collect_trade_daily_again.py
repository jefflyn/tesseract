import datetime
import time
import tushare as ts
from stocks.util.db_util import get_db

from stocks.util.pro_util import pro


def recollect_hist_daily(sql='select b.ts_code, b.code from select_result_all s '
                             'inner join basic b on s.code = b.code where abs(gap) > 12', all=False):
    """
        重新获取除权后的历史数据
        """
    # 建立数据库连接
    db = get_db()
    cursor = db.cursor()
    total = cursor.execute(sql)
    if total == 0:
        print("no stock found, process end!")
        exit(0)

    start_dt = '20150101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=0)
    end_dt = time_temp.strftime('%Y%m%d')
    print("Collect trade data from " + start_dt + " to " + end_dt)

    stock_pool = [ts_code_tuple for ts_code_tuple in cursor.fetchall()]
    ts_codes = [result[0] for result in stock_pool]
    codes = [result[1] for result in stock_pool]
    code_str = ','.join(str(n) for n in codes)
    try:
        if all is False:
            del_sql = 'delete from hist_trade_day where code in (' + code_str + ')'
            print(del_sql)
            succ = cursor.execute(del_sql)
    except Exception as e:
        db.rollback()
        print(e)
        exit(0)
    # stock_pool = ['300594.SZ']
    # 循环获取单个股票的日线行情
    # 1分钟不超过200次调用
    begin_time = datetime.datetime.now()
    for i in range(len(ts_codes)):
        try:
            # 打印进度
            if i % 200 == 0:
                print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(ts_codes[i]))
            if i > 0 and i % 198 == 0:
                end_time = datetime.datetime.now()
                time_diff = (end_time - begin_time).seconds
                sleep_time = 60 - time_diff
                if sleep_time > 0:
                    print('sleep for ' + str(sleep_time) + ' seconds ...')
                    time.sleep(sleep_time)
                begin_time = datetime.datetime.now()
            # 前复权行情
            df = ts.pro_bar(api=pro, ts_code=ts_codes[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            if df is None:
                continue
            c_len = df.shape[0]
        except Exception as e:
            print('Exception: ' + str(e))
            time.sleep(60)
            df = ts.pro_bar(api=pro, ts_code=ts_codes[i], adj='qfq', start_date=start_dt, end_date=end_dt)
            # 打印进度
            print('Redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(ts_codes[i]))
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
                sql_insert = "INSERT INTO hist_trade_day(trade_date,ts_code,code,pre_close,open,close,high,low,vol,amount,amt_change,pct_change) " \
                             "VALUES ('%s', '%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%.2f','%i','%.4f','%.2f','%.4f')" % (
                                 trade_date, str(resu[0]), str(resu[0])[0:6], float(resu[6]), float(resu[2]),
                                 float(resu[5]), float(resu[3]), float(resu[4]),
                                 float(resu[9]), float(resu[10]), float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                db.rollback()
                print(err)
                continue
    cursor.close()
    db.close()
    print('All Finished!')


if __name__ == '__main__':
    # sql = 'select ts_code, code from hist_trade_day where open=0 and high=0'
    sql = 'select ts_code, code from basic where code=300782'
    recollect_hist_daily(sql, False)
    # recollect_hist_daily()
