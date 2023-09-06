import zillion.future.db_util as _dt
from zillion.future.db_util import read_sql
from zillion.utils import date_util


def get_daily(code=None, trade_date=None, start_date=None, end_date=None):
    # 建立数据库连接
    db = _dt.get_db("stock")
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    sql = "select * from stock.trade_daily_us where 1=1 "
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

    df = read_sql(sql, params=params)
    df.index = list(df['code'])
    return df




