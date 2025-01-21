from time import sleep

import tushare as ts

from zillion.stock import db_stock

# 建立数据库连接
db = db_stock.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

# 初始化pro接口
pro = ts.pro_api('f65316bb26b0a27ef7f876249615fcba99b5aab10e5be46cb278e53e')

basic_fields = [
    "ts_code",
    "name",
    "classify",
    "list_date",
    "delist_date",
    "enname",
    "list_status"
]

if __name__ == '__main__':
    cursor.execute("delete from basic_us where 1=1;")
    db.commit()
    offset = 0
    page_size = 0
    for i in range(1, 10):
        param = {"offset": str(offset)}
        df = pro.us_basic(**param, fields=basic_fields)
        if df is None or df.empty:
            break
        db_stock.to_db(df, 'basic_us', if_exists='append')
        db.commit()
        print('save basic_us successfully! offset=' + str(offset))
        size = len(df)
        if size < page_size:
            break
        else:
            page_size = size
        offset += size
        if i % 2 == 0:
            sleep(60)
