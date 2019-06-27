from stocks.base import display
from stocks.base import db_util
from stocks.base.pro_util import pro

if __name__ == '__main__':
    df = pro.cctv_news(date='20190626')
    print(df)
    db_util.to_db(df, 'cctv_news', if_exists='replace')

