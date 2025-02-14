from akshare.stock.stock_us_sina import stock_us_spot

from zillion.stock import db_stock

# 建立数据库连接
db = db_stock.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

if __name__ == '__main__':
    cursor.execute("truncate basic_us")
    db.commit()
    # 美股所有股票实时行情
    df = stock_us_spot()
    db_stock.to_db(df, 'basic_us', if_exists='append')
    db.commit()
