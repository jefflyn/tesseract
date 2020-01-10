# coding=utf-8
import os
import calendar
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
import urllib.request as request
import pandas as pd
import arrow

today = datetime.datetime.now()

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

default_format = '%Y-%m-%d'
format_flat = '%Y%m%d'

hist_date_list = pd.read_csv(os.getenv('STOCKS_HOME') + '/data/etl/basic_data/' + 'hist_trade_date.csv')


utc = arrow.utcnow()
local = utc.to('local')

DATE_FORMAT_MONTH = 'YYYY-MM'
DATE_FORMAT_SIMPLE = 'YYYYMMDD'
DATE_FORMAT_DEFAULT = 'YYYY-MM-DD'
DATE_FORMAT_FULL = 'YYYY-MM-DD HH:mm:ss'

EIGHT_HOURS = 60 * 60 * 8

"""
天
"""
#今天
NOW = local.format(DATE_FORMAT_FULL)

TODAY = local.format(DATE_FORMAT_DEFAULT)
#昨天
YESTERDAY = local.shift(days=-1).format(DATE_FORMAT_DEFAULT)
#7天前
DATE_BEFORE_7_DAYS = local.shift(days=-7).format(DATE_FORMAT_DEFAULT)
DATE_BEFORE_7_DAYS_SIMP = local.shift(days=-7).format(DATE_FORMAT_SIMPLE)
#30天前
DATE_BEFORE_30_DAYS = local.shift(days=-30).format(DATE_FORMAT_DEFAULT)
#60天前
DATE_BEFORE_60_DAYS = local.shift(days=-60).format(DATE_FORMAT_DEFAULT)
#90天前
DATE_BEFORE_90_DAYS = local.shift(days=-90).format(DATE_FORMAT_DEFAULT)

"""
周
"""
#本周第一天
FIRST_DAY_THIS_WEEK = local.floor('week').format(DATE_FORMAT_DEFAULT)
#本周最后一天
LAST_DAY_THIS_WEEK = local.ceil('week').shift(days=-2).format(DATE_FORMAT_DEFAULT)
#上周第一天
FIRST_DAY_LAST_WEEK = local.floor('week').shift(weeks=-1).format(DATE_FORMAT_DEFAULT)
#上周最后一天
LAST_DAY_LAST_WEEK = local.ceil('week').shift(weeks=-1).shift(days=-2).format(DATE_FORMAT_DEFAULT)
#6周前第一天
FIRST_DAY_6_WEEK = local.ceil('week').shift(weeks=-8).shift(days=-2).format(DATE_FORMAT_DEFAULT)

"""
月
"""
#本月第一天
FIRST_DAY_THIS_MONTH = local.floor('month').format(DATE_FORMAT_DEFAULT)
#本月最后一天
LAST_DAY_THIS_MONTH = local.ceil('month').format(DATE_FORMAT_DEFAULT)
#上月第一天
FIRST_DAY_LAST_MONTH = local.floor('month').shift(months=-1).format(DATE_FORMAT_DEFAULT)
#上月最后一天
LAST_DAY_LAST_MONTH = local.ceil('month').shift(months=-1).format(DATE_FORMAT_DEFAULT)
#6个月前第一天
FIRST_DAY_6_MONTH = local.floor('month').shift(months=-6).format(DATE_FORMAT_DEFAULT)
#6个月前最后一天
LAST_DAY_6_MONTH = local.ceil('month').shift(months=-6).format(DATE_FORMAT_DEFAULT)

"""
季度
"""
#今年第1季度
FIR_Q_THIS_YEAR = local.floor('year').format(DATE_FORMAT_DEFAULT)
#今年第2季度
SEC_Q_THIS_YEAR = local.floor('year').shift(months=3).format(DATE_FORMAT_DEFAULT)
#今年第3季度
THIRD_Q_THIS_YEAR = local.floor('year').shift(months=6).format(DATE_FORMAT_DEFAULT)
#今年第4季度
FOUR_Q_THIS_YEAR = local.floor('year').shift(months=9).format(DATE_FORMAT_DEFAULT)

"""
年
"""
#今年第一天
FIRST_DAY_THIS_YEAR = local.floor('year').format(DATE_FORMAT_DEFAULT)
#去年第一天
FIRST_DAY_LAST_YEAR = local.floor('year').shift(years=-1).format(DATE_FORMAT_DEFAULT)
#去年最后一天
LAST_DAY_LAST_YEAR = local.ceil('year').shift(years=-1).format(DATE_FORMAT_DEFAULT)


def parse_datestr(datestr=NOW, format=None):
    if format is None:
        return arrow.get(datestr)
    else:
        return arrow.get(datestr).format(format)


def shift_date(target=local, shiftType='d', n=-1, format=DATE_FORMAT_DEFAULT):
    """
    日期前后滑动
    :param target: arrow
    :param shiftType: d w m y
    :param n:
    :return:
    """
    if shiftType == 'd':
        target = target.shift(days=n)
    elif shiftType == 'w':
        target = target.shift(weeks=n)
    elif shiftType == 'm':
        target = target.shift(months=n)
    elif shiftType == 'y':
        target = target.shift(years=n)
    else:
        print('shift type not found: %s' % shiftType)
    return target.format(format)


def get_now():
    return datetime.datetime.now()


# 本周第一天和最后一天
def get_today(format=default_format):
    return today.strftime(format)


# 本周第一天和最后一天
def get_this_week_start(format=default_format):
    return this_week_start.strftime(format)


def get_this_week_end(format=default_format):
    return this_week_end.strftime(format)


# 上周第一天和最后一天
def get_last_week_start(format=default_format):
    return last_week_start.strftime(format)


def get_last_week_end(format=default_format):
    return last_week_end.strftime(format)


# 本月第一天和最后一天
def get_this_month_start(format=default_format):
    return this_month_start.strftime(format)


def get_this_month_end(format=default_format):
    return this_month_end.strftime(format)


# 上月第一天和最后一天
def get_last_month_start(format=default_format):
    return last_month_start.strftime(format)


def get_last_month_end(format=default_format):
    return last_month_end.strftime(format)


def get_last_2month_start(format=default_format):
    return last_2month_start.strftime(format)


# 本季第一天和最后一天
def get_this_quarter_start(format=default_format):
    return this_quarter_start.strftime(format)


def get_this_quarter_end(format=default_format):
    return this_quarter_end.strftime(format)


# 上季第一天和最后一天
def get_last_quarter_start(format=default_format):
    return last_quarter_start.strftime(format)


def get_last_quarter_end(format=default_format):
    return last_quarter_end.strftime(format)


# 本年第一天和最后一天
def get_this_year_start(format=default_format):
    return this_year_start.strftime(format)


def get_this_year_end(format=default_format):
    return this_year_end.strftime(format)


# 去年第一天和最后一天
def get_last_year_start(format=default_format):
    return last_year_start.strftime(format)


def get_last_year_end(format=default_format):
    return last_year_end.strftime(format)


def parse_date_str(date_str, format=default_format):
    c_date = convert_to_date(date_str)
    return c_date.strftime(format)


def convert_to_date(date_str):
    query_date = datetime.datetime.strptime(date_str, default_format) if len(date_str) > 8 \
        else datetime.datetime.strptime(date_str, format_flat)
    return query_date


def get_day_type(query_date):
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date
    resp = request.urlopen(url)
    content = resp.read()
    if content:
        try:
            day_type = int(content)
        except ValueError:
            return -1
        else:
            return day_type
    else:
        return -1


def get_latest_trade_date(days=1):
    """
    :param days:
    :return: [yyyy-MM-dd]
    """
    trade_dates = hist_date_list[(hist_date_list.is_trade == 1) & (hist_date_list.hist_date <= get_today())].head(days)
    return list(trade_dates['hist_date'])


def is_tradeday(query_date=None):
    hist_date = hist_date_list[(hist_date_list.hist_date == query_date) & (hist_date_list.is_trade == 1)]
    return True if hist_date is not None else False
    # query_date = convert_to_date(query_date)
    # is_holiday = ts_dateu.is_holiday(query_date)
    # return is_holiday is False


def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)


def get_previous_trade_day(trade_date=today):
    """
    获取指定日期上个交易日
    :param trade_date:'yyyy-MM-dd' or 'yyyyMMdd'
    :return: str 'yyyy-MM-dd'
    """
    hist_date = hist_date_list[hist_date_list.hist_date == trade_date]
    if hist_date.empty is True:
        print(trade_date)
    index = hist_date.index.to_numpy()[0]
    for i in range(1, 15):
        next_hist_date = hist_date_list.loc[index + i, ['hist_date', 'is_trade']]
        if next_hist_date[1] == 1:
            return next_hist_date.iat[0]



def get_next_trade_day(trade_date=today):
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
        next_hist_date = hist_date_list.loc[index - i, ['hist_date', 'is_trade']]
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
        target_date = (today - timedelta(days=n)).strftime(format_flat)
        if is_tradeday(target_date):
            start_date = today - timedelta(days=n)
            to_date = (today - timedelta(days=n)).strftime(default_format)
            from_date = None
            for i in range(1, 10):
                target_from_date = (start_date - timedelta(days=i)).strftime(format_flat)
                if is_tradeday(target_from_date):
                    from_date = (start_date - timedelta(days=i)).strftime(default_format)
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
    return [monday.strftime(default_format), friday.strftime(default_format)]


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

    result_list = [(format(current_begin, default_format), format(current_end, default_format))]
    for i in range(howmany - 1):
        current_end = current_begin - timedelta(days=1)
        current_begin = datetime.date(current_end.year, current_end.month, 1)
        result_list.append((format(current_begin, default_format), format(current_end, default_format)))
    result_list = result_list[::-1]
    return result_list



if __name__ == '__main__':
    print(get_next_trade_day('2019-12-06'))
    print(get_previous_trade_day('2019-12-08'))
    # init_trade_date_list()

    print(get_latest_trade_date(5))
    # print(get_month_firstday_lastday(8))
    # print(this_month_start)
    # print(get_week_firstday_lastday(-8))
    # print(get_week_firstday_lastday(-7))
    # print(get_week_firstday_lastday(-6))
    # print(get_week_firstday_lastday(-5))
    # print(get_week_firstday_lastday(-4))
    # print(get_week_firstday_lastday(-3))
    # print(get_week_firstday_lastday(-2))
    # print(get_week_firstday_lastday(-1))
