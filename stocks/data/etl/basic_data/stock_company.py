from stocks.base import display
from stocks.base.pro_util import pro
from stocks.base import db_util

if __name__ == '__main__':
    # SSE-上交所 SZSE-深交所
    df = pro.stock_company(exchange='SSE')
    # print(df)
    db_util.to_db(df, 'stock_company', if_exists='append')
    df = pro.stock_company(exchange='SZSE')
    db_util.to_db(df, 'stock_company', if_exists='append')

