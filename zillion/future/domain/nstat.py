import zillion.utils.db_util as _dt

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

class Nstat:
    symbol = ''
    code = ''
    low = 0
    high = 0

    def __init__(self, symbol, code, low, high):
        self.symbol = symbol
        self.code = code
        self.low = low
        self.high = high


if __name__ == '__main__':
    print(pre_main_contract('A2305', 'A2305'))
