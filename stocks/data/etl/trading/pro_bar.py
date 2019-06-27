from stocks.base import display
import tushare as ts

if __name__ == '__main__':
    """
    https://tushare.pro/document/2?doc_id=109
    """
    # df = ts.pro_bar(ts_code='600773.SH', freq='M', adj='qfq', start_date='20190101', end_date='20191101')
    df = ts.pro_bar(ts_code='002918.SZ', freq='D', adj='qfq')
    print(df)

