import datetime

from stocks.future.future_constants import *
from stocks.util import date_util
from stocks.util.db_util import get_db
from stocks.util.db_util import read_sql


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


def get_future_daily(name=None, trade_date=None):
    sql = "select * from future_daily where 1=1 "
    if name is not None:
        sql += 'and name = :name '
    if trade_date is not None:
        sql += 'and trade_date = :trade_date '
    params = {'name': name, 'trade_date': trade_date}
    df = read_sql(sql, params=params)
    return df


def add_log(name, log_type, pct_change, content, remark):
    print('add log -------------')

    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    try:
        cursor.execute(
            'insert into future_log(name,type,content,pct_change,log_time,remark) '
            'values(%s,%s,%s,%s,%s,%s)', (name, log_type, content, pct_change, date_util.get_now(),
                                          log_type if remark == '' or remark is None else remark))
        db.commit()
    except Exception as err:
        print('>>> failed!', err)
        db.rollback()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    is_trade_time()
