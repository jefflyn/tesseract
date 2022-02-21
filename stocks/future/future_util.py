import datetime

import pandas as pd

from stocks.future import future_trade
from stocks.future.future_constants import *
from stocks.util import date_util
from stocks.util.db_util import get_db
from stocks.util.db_util import read_sql


def select_from_sql(sql=None):
    return read_sql(sql, params=None)


def is_trade_time():
    '''
    日盘 09:00-15:00
    夜盘 21:00-23:00
    :return:
    '''
    current_time = date_util.now()
    morning_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=9, minute=1)
    morning_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=11, minute=30)
    afternoon_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=13, minute=30)
    afternoon_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=15, minute=0)
    night_open_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=21, minute=1)
    night_close_time = datetime.datetime(current_time.year, current_time.month, current_time.day, hour=23, minute=50)

    is_trade_time = (morning_open_time <= date_util.now() <= morning_close_time) or \
                    (afternoon_open_time <= date_util.now() <= afternoon_close_time) or \
                    (night_open_time <= date_util.now() <= night_close_time)
    # print(current_time, day_open_time, day_close_time, night_open_time, night_close_time, is_trade_time)
    return is_trade_time


def get_future_basics(code=None, type=None, night=None, on_target=None):
    '''
    查询商品合约详情，不包含金融产品
    :param code:
    :param type:
    :param night:
    :param on_target:
    :return:
    '''
    sql = "select * from future_basics where deleted = 0 "
    if on_target is True:
        sql += 'and target = :on_target '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if type is not None and type not in ['tar', 'all']:
        sql += 'and goods_type = :type '
    if night is not None:
        sql += 'and night = :night '
    params = {'code': code, 'type': GOODS_TYPE_MAP.get(type), 'night': night, 'on_target': 1}
    df = read_sql(sql, params=params)
    return df


def add_realtime_data(codes=None, local_last_trade_date=None):
    last_trade_date = date_util.get_today(date_util.FORMAT_FLAT)  # .get_latest_trade_date(1)[0]
    if local_last_trade_date < last_trade_date:  # not the latest record
        sina_code = codes[0].split('.')[0]
        realtime = future_trade.realtime(sina_code)
        if realtime is not None and realtime.empty is False:
            realtime['ts_code'] = codes[0]
            realtime['trade_date'] = last_trade_date
            return realtime
    return None


def get_ts_future_daily(ts_code=None, start_date=None, end_date=None):
    sql = "select * from ts_future_daily where 1=1 "
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

    local_last_trade_date = list(df['trade_date'])[-1]
    realtime = add_realtime_data(ts_code, local_last_trade_date)
    if realtime is not None:
        # hist_data = hist_data.append(realtime, ignore_index=True)
        df = pd.concat([df, realtime], ignore_index=True)
    return df


def get_future_daily(name=None, trade_date=None):
    sql = "select * from future_daily where 1=1 "
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
            'insert into future_log(name, type, content, price, position, pct_change, log_time, remark) '
            'values(%s, %s, %s, %s, %s, %s, %s, %s)',
            (name, log_type, content, price, position, pct_change, date_util.get_now(), remark)
        )
        db.commit()
    except Exception as err:
        print('>>> insert future_log failed!', err)
        db.rollback()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    df = get_ts_future_daily(ts_code='PKL.ZCE', start_date=20220127)
    print(df)
