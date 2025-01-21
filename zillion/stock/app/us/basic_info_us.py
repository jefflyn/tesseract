from akshare.stock.stock_us_sina import get_us_page_count, get_us_stock_info
from tqdm import tqdm

from zillion.stock import db_stock

# 建立数据库连接
db = db_stock.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


if __name__ == '__main__':
    # cursor.execute("truncate basic_info_us")
    # db.commit()
    page_count = get_us_page_count()
    for page in tqdm(range(1, page_count + 1)):
        df = get_us_stock_info(page)
        db_stock.to_db(df, 'basic_info_us', if_exists='append')
        db.commit()

