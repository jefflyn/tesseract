import zillion.utils.db_util as _dt
from zillion.utils.db_util import read_sql

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def get_local_contract(code=None, main=False, selected=False):
    sql = "select * from contract where 1=1 "
    if code is not None:
        sql += 'and code = :code '
    if main is True:
        sql += 'and main = 1 '
    if selected is True:
        sql += 'and selected = 1 '
    params = {'code': code, 'main': main, 'selected': selected}
    df = read_sql(sql, params=params)
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
            print('  >>> insert contract error:', err)


def update_contract_main(code):
    sql = "update contract set main=1, update_time=now() where code='%s';"
    cursor.execute(sql % code)
    db.commit()


def remove_contract_hist(code, values=None):
    sql = "delete from contract where code='%s';"
    cursor.execute(sql % code)
    save_contract(values, True)
