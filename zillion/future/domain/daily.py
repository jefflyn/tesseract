import akshare as ak
import numpy as np
import pandas as pd
from akshare.futures.symbol_var import symbol_varieties

import zillion.utils.db_util as _dt
from zillion.utils import date_util
# 建立数据库连接
from zillion.utils.date_util import FORMAT_FLAT

db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def _save_daily(values=None):
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


def get_daily_all_ak(date=None):
    if date is None:
        date = date_util.get_today(FORMAT_FLAT)
    dce_daily = ak.get_dce_daily(date)
    czce_daily = ak.get_czce_daily(date)
    gfex_daily = ak.get_gfex_daily(date)
    ine_daily = ak.get_ine_daily(date)
    shfe_daily = ak.get_shfe_daily(date)
    all_data = pd.concat([dce_daily, czce_daily, gfex_daily, ine_daily, shfe_daily], ignore_index=True)
    print(all_data)


def get_hist_daily_ak(codes=None):
    '''
    历史全量
    :param codes:
    :return:
    '''
    size = len(codes)
    seq = 1
    collect_time = date_util.now()
    for code in codes:
        df_data = ak.futures_zh_daily_sina(code)
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        # replace_values = {'oi': 0, 'oi_chg': 0}
        # df_data.fillna(value=replace_values, inplace=True)
        df_data['settle'] = np.where(df_data.settle > 0, df_data.settle, df_data.close)
        df_data['close'] = np.where(df_data.close > 0, df_data.close, df_data.settle)
        settle_list = list(df_data['settle'])
        settle_list.insert(0, 0)
        settle_list.pop(len(settle_list) - 1)
        close_list = list(df_data['close'])
        close_list.insert(0, 0)
        close_list.pop(len(close_list) - 1)
        df_data['pre_settle'] = settle_list
        df_data['pre_close'] = close_list
        # print(df_data.tail(10))
        data_list = []
        for index, row in df_data.iterrows():
            close_change = round((row['close'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row['pre_settle'] > 0 else 0
            settle_change = round((row['settle'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row['pre_settle'] > 0 else 0
            data_list.append([symbol_varieties(code), row['date'], code,  row['open'], row['high'], row['low'],
                              row['close'], row['settle'], row['pre_close'], row['pre_settle'], close_change, settle_change,
                              row['volume'], row['hold'], collect_time])
        _save_daily(data_list)
        print(str(seq) + "/" + str(size) + " done")
        seq += 1


if __name__ == '__main__':
    get_hist_daily_ak(["A2305"])
