from zillion.future import future_util
from zillion.utils import date_util


if __name__ == '__main__':
    future_basics = future_util.get_future_basics()
    week_end = date_util.get_today(date_util.FORMAT_FLAT)
    week_start = date_util.shift_date_flat_format(n=-30)

    ts_codes = list(future_basics['ts_code'])
    df_data = future_util.get_ts_future_daily(ts_codes, start_date=week_start, end_date=week_end)[
        ['ts_code', 'trade_date', 'pre_close', 'pre_settle', 'open', 'high', 'low', 'close']]

    stat_data = []

