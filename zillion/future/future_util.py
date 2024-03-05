import datetime

import pandas as pd

from zillion.future.db_util import get_db
from zillion.future.db_util import read_sql
from zillion.future.domain import trade
from zillion.utils import date_util


def select_from_sql(sql=None):
    return read_sql(sql, params=None)


def is_trade_time():
    '''
    日盘 09:00-15:00
    夜盘 21:00-23:00
    :return:
    '''
    current_time = date_util.now()
    morning_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=9, minute=0, second=30)
    morning_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=11, minute=30)
    afternoon_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=13, minute=29, second=30)
    afternoon_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=15, minute=0, second=3)
    night_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=21, minute=0, second=30)
    night_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=23, minute=50)

    # print(current_time, day_open_time, day_close_time, night_open_time, night_close_time, is_trade_time)
    return (morning_open_time <= date_util.now() <= morning_close_time) or \
        (afternoon_open_time <= date_util.now() <= afternoon_close_time) or \
        (night_open_time <= date_util.now() <= night_close_time)


def add_realtime_data(codes=None, daily_df=None):
    local_last_daily = daily_df.tail(1)
    last_data = local_last_daily.iloc[0]
    local_last_trade_date = last_data.at['trade_date']
    last_trade_date = date_util.get_today(date_util.FORMAT_FLAT)  # .get_latest_trade_date(1)[0]
    if local_last_trade_date < last_trade_date:  # local not the latest record, add realtime
        realtime_df = None
        for code in codes:
            sina_code = code.split('.')[0]
            realtime = trade.realtime_simple(sina_code)
            if realtime is not None and realtime.empty is False:
                realtime['ts_code'] = code
                realtime['trade_date'] = last_trade_date
                code_data = daily_df[(daily_df.trade_date == local_last_trade_date) & (daily_df.ts_code == code)]
                realtime['pre_close'] = code_data.iloc[0].at['close']
                realtime['pre_settle'] = code_data.iloc[0].at['settle']
                realtime['close_change'] = realtime['close'] - realtime['pre_settle']
                if realtime_df is None:
                    realtime_df = realtime
                else:
                    realtime_df = pd.concat([realtime_df, realtime], ignore_index=True)
        return realtime_df
    return None


def get_ts_future_hist_daily(ts_code=None, start_date=None, end_date=None):
    sql = "select * from ts_trade_daily_hist where 1=1 "
    if ts_code is not None:
        if isinstance(ts_code, str):
            codes = list()
            codes.append(ts_code)
            ts_code = codes
        sql += 'and ts_code in :codes '
    if start_date is not None:
        sql += 'and trade_date >=:start '
    if end_date is not None:
        sql += 'and trade_date <=:end '

    params = {'codes': ts_code, 'start': start_date, 'end': end_date}
    df = read_sql(sql, params=params)
    if df is None or df.empty is True:
        return df
    if end_date is None:
        realtime = add_realtime_data(ts_code, df)
        if realtime is not None:
            # hist_data = hist_data.append(realtime, ignore_index=True)
            df = pd.concat([df, realtime], ignore_index=True)
    return df


def get_ts_future_daily(ts_code=None, start_date=None, end_date=None):
    sql = "select * from ts_trade_daily where 1=1 "
    if ts_code is not None:
        if isinstance(ts_code, str):
            codes = list()
            codes.append(ts_code)
            ts_code = codes
        sql += 'and ts_code in :codes '
    if start_date is not None:
        sql += 'and trade_date >=:start '
    if end_date is not None:
        sql += 'and trade_date <=:end '

    params = {'codes': ts_code, 'start': start_date, 'end': end_date}
    df = read_sql(sql, params=params)
    if df is None or df.empty is True:
        return df
    if end_date is None:
        realtime = add_realtime_data(ts_code, df)
        if realtime is not None:
            # hist_data = hist_data.append(realtime, ignore_index=True)
            df = pd.concat([df, realtime], ignore_index=True)
    return df


def get_future_daily(name=None, trade_date=None):
    sql = "select * from trade_daily where 1=1 "
    if name is not None:
        sql += 'and name = :name '
    if trade_date is not None:
        sql += 'and trade_date = :trade_date '
    params = {'name': name, 'trade_date': trade_date}
    df = read_sql(sql, params=params)
    return df


def add_log(name, log_type, pct_change, content, remark, price=None, position=None):
    print('add log -------------')

    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    try:
        cursor.execute(
            'insert into trade_log(name, type, content, price, position, pct_change, log_time, remark) '
            'values(%s, %s, %s, %s, %s, %s, %s, %s)',
            (name, log_type, content, price, position, pct_change, date_util.now_str(), remark)
        )
        db.commit()
    except Exception as err:
        print('>>> insert trade_log failed!', err)
        db.rollback()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


def calc_position(price, low, high):
    if low == high:
        return 0
    return round((price - low) / (high - low) * 100)


if __name__ == '__main__':
    df = get_ts_future_daily(ts_code='PK2301.ZCE', start_date=20220827)
    print(df)
    val = df.iloc[18].iat[1]
    val2 = df.iat[18, 1]
    print(val, val2)
