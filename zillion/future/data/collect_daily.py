import math

import pandas as pd

import zillion.utils.db_util as _dt
from zillion.utils import date_util, pro_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def save_daily(values=None):
    if values is not None and len(values) > 0:
        try:
            # 注意这里使用的是executemany而不是execute
            insert_sql = 'INSERT INTO future.trade_daily (symbol, trade_date, code, open, high, low, close, settle, ' \
                         'pre_close, pre_settle, close_change, settle_change, deal_vol, hold_vol, create_time) VALUES ' \
                         '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(insert_sql, values)
            db.commit()
        except Exception as err:
            print('  >>> insert daily error:', err)


def add_daily(codes=None):
    size = len(codes)
    seq = 1
    for code in codes:
        df_data = pro_util.pro.fut_daily(code=code)
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        replace_values = {'oi': 0, 'oi_chg': 0}
        df_data.fillna(value=replace_values, inplace=True)
        # data_list = []
        for index, row in df_data.iterrows():
            data_list = []
            close = row['settle'] if math.isnan(row['close']) else row['close']
            pre_close = row['pre_settle'] if math.isnan(row['pre_close']) else row['pre_close']
            open = row['pre_settle'] if math.isnan(row['open']) else row['open']
            high = close if math.isnan(row['high']) else row['high']
            low = close if math.isnan(row['low']) else row['low']
            change1 = row['change2'] if math.isnan(row['change1']) else row['change1']
            data_list.append([row['code'], row['trade_date'], pre_close, row['pre_settle'], open,
                              high, low, close, row['settle'], change1, row['change2'], row['vol'], row['amount'],
                              row['oi'], row['oi_chg'], date_util.now()])
            save_daily(data_list)
        print(str(seq) + "/" + str(size) + " done")
        seq += 1


if __name__ == '__main__':
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()

    code_list = [
        'M2305.DCE','OI2305.ZCE','RM2305.ZCE','Y2305.DCE']
    add_daily(code_list)

    print('done @', date_util.get_now())
