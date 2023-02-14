import zillion.utils.db_util as _dt
from zillion.future.domain import basic
from zillion.utils.db_util import read_sql

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def get_main_contract_code():
    '''
    连续合约
    :return:
    '''
    symbol_exchange_map = basic.symbol_exchange_map(None)
    return [symbol + '0' for symbol in symbol_exchange_map.keys()]


def pre_main_contract(code, main):
    if code[-1] != '0':
        return code < main
    return False


def get_local_contract(symbol=None, code=None, main=False, selected=False):
    sql = "select * from contract where 1=1 "
    if symbol is not None:
        sql += 'and symbol = :symbol '
    if code is not None:
        sql += 'and code = :code '
    if main is True:
        sql += 'and main = 1 '
    if selected is True:
        sql += 'and selected = 1 '
    params = {'symbol': symbol, 'code': code, 'main': main, 'selected': selected}
    df = read_sql(sql, params=params)
    # df['low_time'] = np.where(df.low_time.notnull(), df.low_time, None)
    # df['high_time'] = np.where(df.high_time.notnull(), df.high_time, None)
    return df


def save_contract(values=None, hist=False):
    if values is not None and len(values) > 0:
        table_name = 'contract' if hist is False else 'contract_hist'
        try:
            insert_sql = 'INSERT INTO ' + table_name + ' (symbol, code, ts_code, main, low, high, low_time, high_time, ' \
                                                       'selected, create_time, update_time, deleted) VALUES ' \
                                                       '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(insert_sql, values)
            db.commit()
        except Exception as err:
            print('  >>> insert error:', table_name, err)


def update_contract_main(code):
    sql = "update contract set main=1, update_time=now() where code='%s';"
    cursor.execute(sql % code)
    db.commit()


def update_contract_hl(code, low, low_time, high, high_time):
    sql = "update contract set low=%d, low_time='%s', high=%d, high_time='%s', update_time=now() where code='%s';"
    cursor.execute(sql % (low, low_time, high, high_time, code))
    db.commit()


def remove_contract_hist(code, values=None):
    sql = "delete from contract where code='%s';"
    cursor.execute(sql % code)
    save_contract(values, True)
    print("Remove contract:", code)


if __name__ == '__main__':
    print(pre_main_contract('A2305', 'A2305'))
