import tushare as ts

from stocks.util import date_util
from stocks.util import db_util

if __name__ == '__main__':
    today_str = date_util.get_today()
    try:
        get_day_all = ts.get_day_all(date=today_str)
        get_day_all.insert(0, 'trade_date', value=today_str)
        db_util.to_db(get_day_all, 'today_all', if_exists='replace')
    except Exception as e:
        print('error:', today_str, 'get today all failed', e)

