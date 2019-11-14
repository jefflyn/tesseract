# coding=utf-8
import calendar
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
import urllib.request as request
import tushare.util.dateu as ts_dateu

now = datetime.datetime.now()

# 今天
today = now

# 昨天
yesterday = now - timedelta(days=1)

# 明天
tomorrow = now + timedelta(days=1)

# 当前季度
now_quarter = now.month / 3 if now.month % 3 == 0 else now.month / 3 + 1

# 本周第一天和最后一天
this_week_start = now - timedelta(days=now.weekday())
this_week_end = now + timedelta(days=6 - now.weekday())

# 上周第一天和最后一天
last_week_start = now - timedelta(days=now.weekday() + 7)
last_week_end = now - timedelta(days=now.weekday() + 1)

# 本月第一天和最后一天
this_month_start = datetime.datetime(now.year, now.month, 1)
this_month_end = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1)

# 上月第一天和最后一天
last_month_end = this_month_start - timedelta(days=1)
last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)

last_2month_end = last_month_start - timedelta(days=1)
last_2month_start = datetime.datetime(last_2month_end.year, last_2month_end.month, 1)

# 本季第一天和最后一天
month = (now.month - 1) - (now.month - 1) % 3 + 1
this_quarter_start = datetime.datetime(now.year, month, 1)
this_quarter_end = datetime.datetime(now.year, month + 3, 1) - timedelta(days=1) if month < 10 \
    else datetime.datetime(now.year, 12, 31)

# 上季第一天和最后一天
last_quarter_end = this_quarter_start - timedelta(days=1)
last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)

# 本年第一天和最后一天
this_year_start = datetime.datetime(now.year, 1, 1)
this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)


# 去年第一天和最后一天
last_year_end = this_year_start - timedelta(days=1)
last_year_start = datetime.datetime(last_year_end.year, 1, 1)

default_format = '%Y-%m-%d'
format_flat = '%Y%m%d'


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


def get_latest_trade_date(days=1, format=default_format):
    if days <= 0:
        days = 1
    trade_date_list = list()
    n = 0
    while True:
        target_date = (now - timedelta(days=n)).strftime(format)
        if is_tradeday(target_date):
            trade_date_list.append((now - timedelta(days=n)).strftime(format))
        n += 1
        if len(trade_date_list) == days:
            break
    return trade_date_list


def is_tradeday(query_date):
    query_date = datetime.datetime.strptime(query_date, default_format) if len(query_date) > 8 \
        else datetime.datetime.strptime(query_date, format_flat)
    is_holiday = ts_dateu.is_holiday(query_date)
    return is_holiday is False


def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)


def get_trade_day(nday=-4):
    """
    获取n对上两个交易日日期
    :param n:
    :return: [today, last n day ...]
    """
    n_trade_day_pair = []
    n = 1
    while True:
        target_date = (now - timedelta(days=n)).strftime(format_flat)
        if is_tradeday(target_date):
            start_date = now - timedelta(days=n)
            to_date = (now - timedelta(days=n)).strftime(default_format)
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
    year = now.year
    month = now.month
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
