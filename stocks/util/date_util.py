# coding=utf-8
import calendar
import datetime
from datetime import timedelta

import arrow
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

# hist_date_list = pd.read_csv(os.getenv('STOCKS_HOME') + '/data/etl/basic_data/' + 'hist_trade_date.csv')

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'
FORMAT_DEFAULT = '%Y-%m-%d'
FORMAT_FLAT = '%Y%m%d'
FORMAT_HOUR = '%H:%M'


# 今天
today = datetime.datetime.now()

open_time = datetime.datetime(today.year, today.month, today.day, hour=9, minute=30, second=0)
mid_close_time = datetime.datetime(today.year, today.month, today.day, hour=11, minute=30, second=0)
mid_open_time = datetime.datetime(today.year, today.month, today.day, hour=13, minute=00, second=0)
close_time = datetime.datetime(today.year, today.month, today.day, hour=15, minute=00, second=0)

# 昨天
yesterday = today - timedelta(days=1)

# 明天
tomorrow = today + timedelta(days=1)

# 当前季度
now_quarter = today.month / 3 if today.month % 3 == 0 else today.month / 3 + 1

# 本周第一天和最后一天
this_week_start = today - timedelta(days=today.weekday())
this_week_end = today + timedelta(days=6 - today.weekday())

# 上周第一天和最后一天
last_week_start = today - timedelta(days=today.weekday() + 7)
last_week_end = today - timedelta(days=today.weekday() + 1)

# 本月第一天和最后一天
this_month_start = datetime.datetime(today.year, today.month, 1)
this_month_end = datetime.datetime(today.year, today.month, 31) if today.month == 12 else \
    datetime.datetime(today.year, today.month + 1, 1) - timedelta(days=1)

# 上月第一天和最后一天
last_month_end = this_month_start - timedelta(days=1)
last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)

last_2month_end = last_month_start - timedelta(days=1)
last_2month_start = datetime.datetime(last_2month_end.year, last_2month_end.month, 1)

# 本季第一天和最后一天
month = (today.month - 1) - (today.month - 1) % 3 + 1
this_quarter_start = datetime.datetime(today.year, month, 1)
this_quarter_end = datetime.datetime(today.year, month + 3, 1) - timedelta(days=1) if month < 10 \
    else datetime.datetime(today.year, 12, 31)

# 上季第一天和最后一天
last_quarter_end = this_quarter_start - timedelta(days=1)
last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)

# 本年第一天和最后一天
this_year_start = datetime.datetime(today.year, 1, 1)
this_year_end = datetime.datetime(today.year + 1, 1, 1) - timedelta(days=1)

# 去年第一天和最后一天
last_year_end = this_year_start - timedelta(days=1)
last_year_start = datetime.datetime(last_year_end.year, 1, 1)


def now():
    return datetime.datetime.now()


def get_now():
    return now().strftime(FORMAT_DATETIME)


def get_now_hour():
    return now().strftime(FORMAT_HOUR)


# 本周第一天和最后一天
def get_today(format=FORMAT_DEFAULT):
    return now().strftime(format)


# 本周第一天和最后一天
def get_this_week_start(format=FORMAT_DEFAULT):
    return (now() - timedelta(days=now().weekday())).strftime(format)


def get_this_week_end(format=FORMAT_DEFAULT):
    return (now() + timedelta(days=6 - now().weekday())).strftime(format)


# 上周第一天和最后一天
def get_last_week_start(format=FORMAT_DEFAULT):
    return (now() - timedelta(days=now().weekday() + 7)).strftime(format)


def get_last_week_end(format=FORMAT_DEFAULT):
    return (now() - timedelta(days=now().weekday() + 1)).strftime(format)


# 本月第一天和最后一天
def get_this_month_start(format=FORMAT_DEFAULT):
    return this_month_start.strftime(format)


def get_this_month_end(format=FORMAT_DEFAULT):
    return this_month_end.strftime(format)


# 上月第一天和最后一天
def get_last_month_start(format=FORMAT_DEFAULT):
    return last_month_start.strftime(format)


def get_last_month_end(format=FORMAT_DEFAULT):
    return last_month_end.strftime(format)


def get_previous_month_end(date=None, format=FORMAT_DEFAULT):
    """
    获取指定日期上个月底
    :param date:
    :param format:
    :return:
    """
    this_date = convert_to_date(date)
    month_start = datetime.datetime(this_date.year, this_date.month, 1)
    previous_month_end = month_start - timedelta(days=1)
    return previous_month_end.strftime(format)


def get_previous_month_trade_end(date=None, format=FORMAT_DEFAULT):
    pre_month_end = get_previous_month_end(date, format)
    return pre_month_end if is_tradeday(pre_month_end) else get_previous_trade_day(pre_month_end)


def get_last_2month_start(format=FORMAT_DEFAULT):
    return last_2month_start.strftime(format)


# 本季第一天和最后一天
def get_this_quarter_start(format=FORMAT_DEFAULT):
    return this_quarter_start.strftime(format)


def get_this_quarter_end(format=FORMAT_DEFAULT):
    return this_quarter_end.strftime(format)


# 上季第一天和最后一天
def get_last_quarter_start(format=FORMAT_DEFAULT):
    return last_quarter_start.strftime(format)


def get_last_quarter_end(format=FORMAT_DEFAULT):
    return last_quarter_end.strftime(format)


# 本年第一天和最后一天
def get_this_year_start(format=FORMAT_DEFAULT):
    return this_year_start.strftime(format)


def get_this_year_end(format=FORMAT_DEFAULT):
    return this_year_end.strftime(format)


# 去年第一天和最后一天
def get_last_year_start(format=FORMAT_DEFAULT):
    return last_year_start.strftime(format)


def get_last_year_end(format=FORMAT_DEFAULT):
    return last_year_end.strftime(format)


def parse_date_str(date_str, format=FORMAT_DEFAULT):
    c_date = convert_to_date(date_str)
    return c_date.strftime(format)


def convert_to_date(date_str):
    query_date = datetime.datetime.strptime(date_str, FORMAT_DEFAULT) if len(date_str) > 8 \
        else datetime.datetime.strptime(date_str, FORMAT_FLAT)
    return query_date


def get_latest_trade_date(days=1):
    """
    :param days:
    :return: [yyyy-MM-dd]
    """
    trade_dates = hist_date_list[(hist_date_list.is_open == 1) & (hist_date_list.hist_date <= get_today())].head(days)
    return list(trade_dates['hist_date'])


def is_tradeday(query_date=None):
    hist_date = hist_date_list[(hist_date_list.hist_date == query_date) & (hist_date_list.is_open == 1)]
    is_open = False if (hist_date is None or hist_date.empty) else True
    # query_date = convert_to_date(query_date)
    # is_holiday = ts_dateu.is_holiday(query_date)
    # return is_holiday is False
    return is_open


def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)


def get_previous_trade_day(trade_date=None):
    """
    获取指定日期上个交易日
    :param trade_date:'yyyy-MM-dd' or 'yyyyMMdd'
    :return: str 'yyyy-MM-dd'
    """
    if trade_date is None:
        trade_date = get_today()
    hist_date = hist_date_list[hist_date_list.hist_date == trade_date]
    if hist_date.empty is True:
        print(trade_date)
    index = hist_date.index.to_numpy()[0]
    for i in range(1, 15):
        next_hist_date = hist_date_list.loc[index + i, ['hist_date', 'is_open']]
        if next_hist_date[1] == 1:
            return next_hist_date.iat[0]


def get_next_trade_day(trade_date=get_today()):
    """
    获取指定日期下个交易日
    :param trade_date:'yyyy-MM-dd'
    :return: str 'yyyy-MM-dd'
    """
    hist_date = hist_date_list[hist_date_list.hist_date == trade_date]
    index = hist_date.index.to_numpy()[0]
    for i in range(1, 15):
        if index - i < 0:
            break
        next_hist_date = hist_date_list.loc[index - i, ['hist_date', 'is_open']]
        if next_hist_date[1] == 1:
            return next_hist_date.iat[0]


def get_trade_day(nday=-4):
    """
    获取n对上两个交易日日期
    :param n:
    :return: [today, last n day ...]
    """
    n_trade_day_pair = []
    n = 1
    while True:
        target_date = (today - timedelta(days=n)).strftime(FORMAT_FLAT)
        if is_tradeday(target_date):
            start_date = today - timedelta(days=n)
            to_date = (today - timedelta(days=n)).strftime(FORMAT_DEFAULT)
            from_date = None
            for i in range(1, 10):
                target_from_date = (start_date - timedelta(days=i)).strftime(FORMAT_FLAT)
                if is_tradeday(target_from_date):
                    from_date = (start_date - timedelta(days=i)).strftime(FORMAT_DEFAULT)
                    break
            n_trade_day_pair.append([from_date, to_date])
        n += 1
        if len(n_trade_day_pair) == abs(nday) or nday == 0:
            break
    return n_trade_day_pair[::-1]


def get_week_firstday_lastday(which=-1):
    """
    获取一周的周一和周五的日期
    :param which:
    :return:
    """
    if which == 0:
        which = 1
    monday = today + relativedelta(weekday=MO(which))
    friday = today + relativedelta(weekday=FR(which))
    return [monday.strftime(FORMAT_DEFAULT), friday.strftime(FORMAT_DEFAULT)]


def get_month_firstday_lastday(howmany=12):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    year = today.year
    month = today.month
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    current_begin = datetime.date(year=year, month=month, day=1)
    current_end = datetime.date(year=year, month=month, day=monthRange)

    result_list = [(format(current_begin, FORMAT_DEFAULT), format(current_end, FORMAT_DEFAULT))]
    for i in range(howmany - 1):
        current_end = current_begin - timedelta(days=1)
        current_begin = datetime.date(current_end.year, current_end.month, 1)
        result_list.append((format(current_begin, FORMAT_DEFAULT), format(current_end, FORMAT_DEFAULT)))
    result_list = result_list[::-1]
    return result_list


def date_diff(begin_date=now(), end_date=now(), type='days'):
    if type == 'days':
        return (end_date - begin_date).days
    elif type == 'minutes':
        return (end_date - begin_date).minutes


def shift_date(type='d', from_date=None, n=-1, format='YYYY-MM-DD'):
    """
    :param type: d w m y
    :param from_date:
    :param n:
    :param format:
    :return:
    """
    utc = arrow.utcnow()
    if from_date is not None:
        utc = utc.strptime(date_str=from_date, fmt='%Y-%m-%d')
    local = utc.to('local')
    if type == 'd':
        target = local.shift(days=n)
    elif type == 'w':
        target = local.shift(weeks=n)
    elif type == 'm':
        target = local.shift(months=n)
    elif type == 'y':
        target = local.shift(years=n)
    return target.format(format)


if __name__ == '__main__':
    print(get_now_hour())
    print(get_next_trade_day('2019-12-06'))
    print(get_previous_trade_day('2019-12-08'))
    # init_trade_date_list()
    print(get_latest_trade_date(5))
    # print(get_month_firstday_lastday(8))
    print(get_previous_month_end('2020-12-31'))
    # print(get_week_firstday_lastday(-8))
    # print(get_week_firstday_lastday(-7))
    # print(get_week_firstday_lastday(-6))
    # print(get_week_firstday_lastday(-5))
    # print(get_week_firstday_lastday(-4))
    # print(get_week_firstday_lastday(-3))
    # print(get_week_firstday_lastday(-2))
    # print(get_week_firstday_lastday(-1))
