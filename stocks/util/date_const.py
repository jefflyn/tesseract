import arrow
from stocks.util.logging import logger

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
        logger.error('shift type not found: %s' % shiftType)
    return target.format(format)


if __name__ == '__main__':
    print(THIRD_Q_THIS_YEAR)
    print(FOUR_Q_THIS_YEAR)
    print(parse_datestr())
    print(parse_datestr(format=DATE_FORMAT_DEFAULT))
    print(shift_date(target=parse_datestr(), shiftType='w'))
    print([shift_date(target=parse_datestr(LAST_DAY_6_MONTH), shiftType='m', n=n, format=DATE_FORMAT_MONTH) for n in range(6)])
