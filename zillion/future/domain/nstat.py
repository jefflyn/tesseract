import zillion.utils.db_util as _dt

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()




if __name__ == '__main__':
    print(pre_main_contract('A2305', 'A2305'))
