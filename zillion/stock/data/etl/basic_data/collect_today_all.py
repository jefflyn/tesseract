import tushare as ts

from zillion.future import db_util
from zillion.utils import date_util

if __name__ == '__main__':
    today_str = date_util.get_today()
    try:
        get_day_all = ts.get_day_all(date=today_str)
        get_day_all.insert(0, 'trade_date', value=today_str)
        db_util.to_db(get_day_all, 'today_all', if_exists='replace')
        print(today_str, 'get today all finished')
    except Exception as e:
        pre_trade_date = date_util.get_previous_trade_day()
        print('error:', today_str, 'get today all failed,', e, 'retry previous trade date', pre_trade_date)
        get_day_all = ts.get_day_all(date=pre_trade_date)
        get_day_all.insert(0, 'trade_date', value=pre_trade_date)
        db_util.to_db(get_day_all, 'today_all', if_exists='replace')
