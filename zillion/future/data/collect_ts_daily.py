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
            insert_sql = 'INSERT INTO ts_trade_daily (ts_code, trade_date, pre_close, pre_settle, ' \
                         'open, high, low, close, settle, close_change, settle_change, deal_vol, deal_amount, ' \
                         'hold_vol, hold_change, create_time) ' \
                         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(insert_sql, values)
            db.commit()
        except Exception as err:
            print('  >>> insert ts daily error:', err)


def add_daily(ts_codes=None):
    size = len(ts_codes)
    seq = 1
    for code in ts_codes:
        df_data = pro_util.pro.fut_daily(ts_code=code)
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
            data_list.append([row['ts_code'], row['trade_date'], pre_close, row['pre_settle'], open,
                              high, low, close, row['settle'], change1, row['change2'], row['vol'], row['amount'],
                              row['oi'], row['oi_chg'], date_util.now()])
            save_daily(data_list)
        print(str(seq) + "/" + str(size) + " done")
        seq += 1


if __name__ == '__main__':
    import akshare as ak

    get_futures_daily_df = ak.get_dce_daily(date="20230104")
    print(get_futures_daily_df)
    # get_futures_daily_df = ak.get_futures_daily(start_date="20220101", end_date="20221231", market="DCE")
    # print(get_futures_daily_df)
    futures_zh_daily_sina_df = ak.futures_zh_daily_sina(symbol="SI2308")
    print(futures_zh_daily_sina_df)
    # futures_zh_spot_df = ak.futures_zh_spot(symbol='TA2305, P2305, B2305, M2305', market="CF", adjust='0')
    # print(futures_zh_spot_df)
    # futures_contract_detail_df = ak.futures_display_main_sina()
    # print(futures_contract_detail_df)
    # futures_main_sina_hist = ak.futures_main_sina(symbol="V0", start_date="20230101", end_date="20230106")
    # print(futures_main_sina_hist)
    # main_contract = ak.match_main_contract(symbol="shfe")
    # print(main_contract)
    # futures_spot_price_df = ak.futures_spot_price(date="2023-01-04")
    # print(futures_spot_price_df)
    # futures_comm_info_df = ak.futures_comm_info(symbol="P2305")
    # print(futures_comm_info_df)

    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()

    ts_code_list = [
        'M2305.DCE','OI2305.ZCE','RM2305.ZCE','Y2305.DCE'
]
    # add_daily(ts_code_list)

    print('done @', date_util.get_now())
