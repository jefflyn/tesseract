from stocks.future.future_constants import *
from stocks.util import date_util
from stocks.util.db_util import get_db
from stocks.util.db_util import read_sql


def get_future_basics(code=None, type=None, night=None, on_target=None):
    '''
    查询商品合约详情，不包含金融产品
    :param code:
    :param type:
    :param night:
    :param on_target:
    :return:
    '''
    sql = "select * from future_basics where 1=1 and deleted = 0 "
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


def add_log(name, log_type, content):
    print('add log -------------')

    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    try:
        cursor.execute(
            'insert into future_log(name,type,content,log_time) '
            'values(%s,%s,%s,%s)', (name, log_type, content, date_util.get_now()))
        db.commit()
    except Exception as err:
        print('>>> failed!', err)
        db.rollback()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()
