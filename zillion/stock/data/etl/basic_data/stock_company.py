from zillion.utils import db_util
from zillion.utils.pro_util import pro

if __name__ == '__main__':
    # SSE-上交所 SZSE-深交所
    df = pro.stock_company(exchange='SSE')
    # print(df)
    db_util.to_db(df, 'stock_company', if_exists='replace')
    df = pro.stock_company(exchange='SZSE')
    db_util.to_db(df, 'stock_company', if_exists='append')

