import zillion.future.db_util as _dt
from zillion.future.db_util import read_sql
from zillion.future.future_constants import GOODS_TYPE_MAP

# 建立数据库连接
db = _dt.get_db("future")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def get_all():
    sql = "select * from basic"
    return read_sql(_dt.DB_FUTURE, sql, params={})


def get_future_basics(type=None, night=None, on_target=None):
    '''
    查询商品合约详情，不包含金融产品
    :param type:
    :param night:
    :param on_target:
    :return:
    '''
    sql = "select * from basic where deleted = 0 "
    if on_target is True:
        sql += 'and target = :on_target '
    if type is not None and type not in ['tar', 'all']:
        sql += 'and goods_type = :type '
    if night is not None:
        sql += 'and night = :night '
    params = {'type': GOODS_TYPE_MAP.get(type), 'night': night, 'on_target': 1}
    df = read_sql(_dt.DB_FUTURE, sql, params=params)
    df.index = df["symbol"]
    return df


def add_basic(values=None):
    '''
    :param values: []
    :return:
    '''
    if values is not None and len(values) > 0:
        try:
            insert_sql = 'INSERT INTO basic (symbol, name, exchange, update_time) VALUES (%s, %s, %s, %s)'
            cursor.execute(insert_sql, values)
            db.commit()
        except Exception as err:
            print('  >>> insert error:', err)


def symbol_exchange_map(basic_df):
    if basic_df is None:
        basic_df = get_future_basics()
    result_map = {}
    for index, row in basic_df.iterrows():
        symbol = row['symbol']
        exchange = row['exchange']
        result_map[symbol] = exchange
    return result_map


if __name__ == '__main__':
    print(symbol_exchange_map(None))
