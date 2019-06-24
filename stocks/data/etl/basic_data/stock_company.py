from stocks.base import display
from stocks.base.pro_util import pro

if __name__ == '__main__':
    # SSE-上交所 SZSE-深交所
    df = pro.stock_company(exchange='SZSE')
    print(df)

