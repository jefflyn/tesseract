from datetime import datetime

import akshare as ak
import numpy as np
import pandas as pd
from akshare.futures import cons
from akshare.futures.symbol_var import symbol_varieties

import zillion.future.db_util as _dt
from zillion.future.db_util import read_sql
from zillion.future.domain import trade
from zillion.utils import date_util
from zillion.utils.date_util import FORMAT_FLAT

# 建立数据库连接
db = _dt.get_db("future")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def delete_daily(code):
    sql = "delete from trade_daily where code='%s';"
    cursor.execute(sql % code)
    db.commit()
    print("Delete gap record ", code)


def _save_daily(values=None):
    if values is not None and len(values) > 0:
        trade_dates = ','.join(set(["'" + e[1] + "'" for e in values]))
        codes = ','.join(set(["'" + e[2] + "'" for e in values]))
        try:
            delete_sql = "delete from trade_daily where code in (" + codes \
                         + ") and trade_date in (" + trade_dates + ");"
            cursor.execute(delete_sql)
            # 注意这里使用的是executemany而不是execute
            insert_sql = 'INSERT INTO future.trade_daily (symbol, trade_date, code, open, high, low, close, settle, ' \
                         'pre_close, pre_settle, close_change, settle_change, deal_vol, hold_vol, create_time) VALUES ' \
                         '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(insert_sql, values)
            db.commit()
        except Exception as err:
            print('  >>> insert daily error:', err)


def _daily_all_ak(date=None):
    if date is None:
        date = cons.get_latest_data_date(date_util.now())
    dce_daily = ak.get_dce_daily(date)
    czce_daily = ak.get_czce_daily(date)
    gfex_daily = ak.get_gfex_daily(date)
    ine_daily = ak.get_ine_daily(date)
    shfe_daily = ak.get_shfe_daily(date)
    all_data = pd.concat([dce_daily, czce_daily, gfex_daily, ine_daily, shfe_daily], ignore_index=True)
    return all_data


def get_pre_trading(codes=None):
    now = date_util.now()
    if 21 <= now.hour <= 23:
        pre_trade_date = cons.get_latest_data_date(now)
    else:
        open_time = datetime(now.year, now.month, now.day, hour=9, minute=0, second=0)
        pre_trade_date = cons.get_latest_data_date(open_time)
    return get_daily(code=codes, trade_date=pre_trade_date)


def get_daily(code=None, trade_date=None, start_date=None, end_date=None):
    sql = "select * from trade_daily where 1=1 "
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :codes '
    if trade_date is not None:
        trade_date = date_util.parse_date_str(trade_date)
        sql += 'and trade_date =:trade_date '
    if start_date is not None:
        start_date = date_util.parse_date_str(start_date)
        sql += 'and trade_date >=:start '
    if end_date is not None:
        end_date = date_util.parse_date_str(end_date)
        sql += 'and trade_date <=:end '
    params = {'codes': code, 'trade_date': trade_date, 'start': start_date, 'end': end_date}

    df = read_sql(_dt.DB_FUTURE, sql, params=params)
    df.index = list(df['code'])
    return df


def collect_daily_ak(codes=None, trade_date=None):
    '''
    日增量
    :param trade_date:
    :param codes:
    :return:
    '''
    last_trade_date = cons.last_trading_day(date_util.parse_date_str(trade_date, FORMAT_FLAT))
    last_trade_data = get_daily(trade_date=last_trade_date)

    size = len(codes)
    seq = 1
    collect_time = date_util.now()
    # all_daily_df = _daily_all_ak(date=trade_date)
    for code in codes:
        # df_data = all_daily_df[(all_daily_df.symbol.str.upper() == code) & (all_daily_df.date == trade_date)]
        df_data = trade.realtime_for_daily(code)
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        # realtime_date = date_util.parse_date_str(df_data.head(1).loc[0, 'date'])
        # if df_data is None or df_data.empty or date_util.parse_date_str(trade_date) != realtime_date:
        #     print(code + ' no daily data!')
        #     continue
        df_index = list(last_trade_data.index)
        if code not in df_index:
            print(code, " pre daily data not found! Refresh hist data!")
            collect_hist_daily_ak([code])
            continue
        pre_close = last_trade_data.loc[code, 'close'] if last_trade_data.empty is False else None


        df_data['pre_close'] = pre_close
        data_list = []
        for index, row in df_data.iterrows():
            close_change = round((row['close'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row[
                                                                                                         'pre_settle'] > 0 else 0
            settle_change = round((row['settle'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row[
                                                                                                           'pre_settle'] > 0 else 0
            data_list.append([symbol_varieties(code), trade_date, code, row['open'], row['high'], row['low'],
                              row['close'], row['settle'], row['pre_close'], row['pre_settle'], close_change,
                              settle_change,
                              row['volume'], row['hold'], collect_time])
        _save_daily(data_list)
        print("processing " + str(seq) + "/" + str(size) + " done!")
        seq += 1


def collect_hist_daily_ak(codes=None):
    '''
    历史全量
    :param codes:
    :return:
    '''
    size = len(codes)
    seq = 1
    collect_time = date_util.now()
    for code in codes:
        df_data = None
        try:
            df_data = ak.futures_zh_daily_sina(code)
        except Exception as e:
            print(code + ' futures_zh_daily_sina error, retry:', e)
            # df_data = ak.futures_zh_daily_sina(code)
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
            close_change = round((row['close'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row[
                                                                                                         'pre_settle'] > 0 else 0
            settle_change = round((row['settle'] - row['pre_settle']) * 100 / row['pre_settle'], 2) if row[
                                                                                                           'pre_settle'] > 0 else 0
            data_list.append([symbol_varieties(code), row['date'], code, row['open'], row['high'], row['low'],
                              row['close'], row['settle'], row['pre_close'], row['pre_settle'], close_change,
                              settle_change,
                              row['volume'], row['hold'], collect_time])
        _save_daily(data_list)
        print(code, "processing " + str(seq) + "/" + str(size) + " done!")
        seq += 1


if __name__ == '__main__':
    # get_pre_trading([])
    collect_hist_daily_ak(["SA2405"])
    # collect_daily_ak(["SA2405"], cons.get_latest_data_date(date_util.now()))


