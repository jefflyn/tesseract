import zillion.utils.db_util as _dt
from zillion.future.domain import basic
from zillion.utils.db_util import read_sql

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()
contract_map = {}


class Contract:
    symbol = ''
    code = ''
    low = 0
    low_date = ''
    high = 0
    high_date = ''

    def __init__(self, symbol, code, low, low_date, high, high_date):
        self.symbol = symbol
        self.code = code
        self.low = low
        self.low_date = low_date
        self.high = high
        self.high_date = high_date


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
    df.index = df["code"]
    return df


def refresh_contract_map(contract_df):
    for index, row in contract_df.iterrows():
        contract_map[index] = Contract(row['symbol'], row['code'], row['low'], row['low_time'][0, 10],
                                       row['high'], row['high_time'][0, 10])


contract_df = get_local_contract()
refresh_contract_map(contract_df)


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


def update_contract_hl(code, low=None, low_time=None, high=None, high_time=None):
    if low is not None and low_time is not None:
        sql = "update contract set low=%d, low_time='%s', update_time=now() where code='%s' and `low` > " + str(low)
        result = cursor.execute(sql % (low, low_time, code))
    if high is not None and high_time is not None:
        sql = "update contract set high=%d, high_time='%s', update_time=now() where code='%s' and `high` < " + str(high)
        result = cursor.execute(sql % (high, high_time, code))
    db.commit()
    refresh_contract_map(get_local_contract(code=code))
    return result


def remove_contract_hist(code, values=None):
    sql = "delete from contract where code='%s';"
    cursor.execute(sql % code)
    save_contract(values, True)
    print("Remove contract:", code)


if __name__ == '__main__':
    print(pre_main_contract('A2305', 'A2305'))
