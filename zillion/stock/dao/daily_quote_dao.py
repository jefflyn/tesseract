import zillion.utils.db_util as _dt
from utils.datetime import date_util
from zillion.db.DataSourceFactory import session_stock
from zillion.utils.db_util import read_sql


class DailyQuoteDAO:
    def __init__(self, session):
        self.session = session


    @staticmethod
    def get_daily(label, code=None, trade_date=None, start_date=None, end_date=None):
        if label == 'a':
            table = 'daily_quote_a'
        elif label == 'hk':
            table = 'daily_quote_hk'
        elif label == 'us':
            table = 'daily_quote_us'
        else:
            table = ''
        sql = "select * from stock." + table + " where 1=1 "
        if code is not None:
            if isinstance(code, str):
                codes = list()
                codes.append(code)
                code = codes
            sql += 'and code in :codes '
        if trade_date is not None:
            trade_date = date_util.parse_date_str(trade_date)
            sql += 'and date =:trade_date '
        if start_date is not None:
            start_date = date_util.parse_date_str(start_date)
            sql += 'and date >=:start '
        if end_date is not None:
            end_date = date_util.parse_date_str(end_date)
            sql += 'and date <=:end '
        params = {'codes': code, 'trade_date': trade_date, 'start': start_date, 'end': end_date}

        df = read_sql(_dt.DB_STOCK, sql, params=params)
        df.index = list(df['code'])
        return df


if __name__ == '__main__':
    daily_quote_dao = DailyQuoteDAO(session_stock)
    df = daily_quote_dao.get_daily(table='daily_quote_a', code='000001', start_date='2019-01-01', end_date='2019-01-31')
    print(df)



