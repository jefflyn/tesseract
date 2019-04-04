import datetime
import pandas as pd

import tushare as ts
from stocks.base.logging import logger as log
import stocks.base.date_const as _dt
from stocks.base.db_util import read_sql
from stocks.base.db_util import read_query

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')
yeardays = datetime.timedelta(days=-365)
oneyearago = (datetime.datetime.now() + yeardays).strftime('%Y%m%d')
oneweek = datetime.timedelta(days=-7)
weekago = (datetime.datetime.now() + oneweek).strftime('%Y%m%d')

INDEX_DICT = {'000001': '上证指数', '000016': '上证50', '000300': '沪深300',
              '399001': '深证成指', '399005': '中小板指', '399006': '创业板指'}
INDEX_LIST = ['000001.SH', '000300.SH', '000016.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399008.SZ']

basics = read_sql("select * from basic", params=None)


def get_monitor_stocks():
    df = read_query('select * from monitor_trigger')
    return df


def get_app_codes():
    df = get_my_stock_pool()
    codes = list(df['code'])
    return codes


def get_limitup_code(period_type='m', period='2019-01', times=3):
    sql = 'select distinct code from limitup_stat where period_type=:type and period=:period and times>=:times'
    params = {'type': period_type, 'period': period, 'times': times}
    log.info(sql + ' ' + str(params))
    df = read_sql(sql, params=params)
    return df


def get_ma_code(grade='a'):
    sql = 'select distinct b.code from hist_ma_day m join basic b on m.ts_code = b.ts_code where rank=:grade'
    params = {'grade': grade}
    log.info(sql + ' ' + str(params))
    df = read_sql(sql, params=params)
    return df


def get_my_stock_pool(type=None, hold=1):
    sql = 'select * from my_stock_pool where 1=1 and is_hold=:hold'
    params = {'hold': hold}
    if type is not None:
        params['type'] = type
        sql = sql + ' and platform=:type'
    log.info(sql + ' ' + str(params))
    df = read_sql(sql, params=params)
    return df


def get_code_by_concept(name=''):
    name_str = '%' + name + '%'
    params = {'name': name_str}
    sql = 'select distinct b.code, b.name from concept c ' \
          'inner join concept_detail d on c.code = d.concept_code ' \
          'inner join basic b on d.ts_code = b.ts_code ' \
          'where c.name like :name'
    df = read_sql(sql, params=params)
    log.info(sql + ' ' + str(params))
    codes = list(df['code'])
    return codes


def get_code_by_industry(industry=None):
    if industry is not None:
        data = basics[basics.industry == industry]
    return list(data['code'])


def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''


def get_letter(string, upper=True):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    try:
        return (''.join(charLst)).upper() if upper else ''.join(charLst)
    except:
        charstr = ''
        for c in lst:
            charstr += str(c)
        return charstr


def get_subnew(cyb=True, list_date=None):
    """
    marketTimeFrom: yyyymmdd
    """
    if list_date is None:
        list_date = oneyearago

    """& (_bsc.list_date < int(weekago))]
    """
    _bsc = basics[(basics.list_date >= int(list_date))]
    # filter unused code
    if cyb is False:
        _bsc = _bsc[_bsc['code'].str.get(0) != '3']
    return _bsc


def format_percent(df=None, columns=[], precision=2):
    if df is None:
        return None
    for columm in columns:
        df[columm] = df[columm].apply(lambda x: str(round(x, precision)) + '%')


def get_sz50():
    sz50df = ts.get_sz50s()
    return list(sz50df['code'])


def get_totay_quotations(datestr=None):
    return ts.get_day_all(date=datestr)


def get_all_codes(cyb=False):
    _bsc = get_basics(cyb=cyb)
    return list(_bsc['code'])


def get_hist_trade(code=None, start=None, end=None):
    sql = 'select * from hist_trade_day where 1=1 '
    if code is not None:
        sql += 'and code =:code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '
    params = {'code': code, 'start': start, 'end': end}
    log.info(sql + ' ' + str(params))
    df = read_sql(sql, params=params)
    return df


def get_k_data(code=None, start=None, end=None):
    hist_data = ts.get_k_data(code, start, end)  # one day delay issue, use realtime interface solved
    if hist_data is None or len(hist_data) == 0:
        print(code + ' k data not found')
        return None
    try:
        latestdate = hist_data.tail(1).at[hist_data.tail(1).index.get_values()[0], 'date']
        if todaystr != latestdate:
            # get today data from [get_realtime_quotes(code)]
            realtime = ts.get_realtime_quotes(code)
            rt_date = realtime.at[0, 'date']
            if latestdate == rt_date:
                return hist_data
            # ridx = realtime.index.get_values()[0]
            todaylow = float(realtime.at[0, 'low'])
            if todaylow > 0:
                newone = {'date': todaystr, 'open': float(realtime.at[0, 'open']),
                          'close': float(realtime.at[0, 'price']),
                          'high': float(realtime.at[0, 'high']), 'low': todaylow,
                          'volume': int(float(realtime.at[0, 'volume']) / 100), 'code': code}
                newdf = pd.DataFrame(newone, index=[0])
                hist_data = hist_data.append(newdf, ignore_index=True)
        return hist_data
    except:
        print(code + ' get k data found exception!')
        return None


def get_data(filepath=None, encoding='gbk', sep=','):
    data = pd.read_csv(filepath, sep=sep, encoding=encoding)
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data


def get_basics(code=None, cyb=True, index=False, before=None):
    """
    index: code
    """
    if index:
        return INDEX_DICT[code]
    data = filter_basic(_basics=basics, cyb=cyb, before=before)

    if code is not None:
        data = data[data.code == code]
    data.index = list(data['code'])
    return data


def get_bottom():
    try:
        data = pd.read_csv("../data/bottom.csv", encoding="utf-8")
        data['code'] = data['code'].astype('str').str.zfill(6)
        return data
    except:
        print('bottom file not found, return empty code list.')
        return pd.DataFrame(columns=['code'])


# filter cyb
def filter_cyb(datadf):
    datadf = datadf[datadf['code'].str.get(0) != '3']
    return datadf


def filter_basic(_basics=None, cyb=True, before=None):
    # filter unused code
    if cyb is False:
        _basics = _basics[_basics['code'].str.get(0) != '3']
    if before is not None:
        _basics = _basics[(_basics['list_date'] > 0) & (_basics['list_date'] <= before)]
    else:
        before = _dt.DATE_BEFORE_7_DAYS_SIMP
        _basics = _basics[(_basics['list_date'] > 0) & (_basics['list_date'] <= int(before))]
    return _basics


def isnumber(a):
    try:
        float(a)
        return True
    except Exception as e:
        return False


def format_amount(amount=None):
    if isnumber(amount) is False:
        return amount
    amtstr = str(amount)
    length = len(amtstr)
    if '.' in amtstr:
        length = len(amtstr.split('.')[0])

    if length < 5:
        return amtstr
    elif length < 9:
        result = round(amount / 10000, 1)
        return str(result) + '万'
    else:
        result = round(amount / (10000 * 10000), 1)
        return str(result) + '亿'


if __name__ == '__main__':
    k_data = ts.get_k_data('000836', ktype='W')
    print(k_data)
    print(format_amount(''))
    print(format_amount(None))
    print(format_amount(12.23))
    print(format_amount(12.2389999989))
    print(format_amount(1236))
    print(format_amount(32589))
    print(format_amount(325862))
    print(format_amount(2369852))
    print(format_amount(25896325))
    print(format_amount(369852369))
    print(format_amount(3628523869.9236))
    # data = get_stock_data(type='c', filename='小金属.txt')
    # trade = pd.HDFStore('trade.h5')
    # tradecomp = pd.HDFStore('trade_comp.h5')
    # limitups = pd.read_hdf('trade.h5', 'hist')
    # df = tradecomp.select('hist')
    # df = df[(df.p_change > 9.9) & (df['code'].str.get(0) != '3')][['code']]
    # df = df.drop_duplicates(['code'])
    # print(df)
    # df1 = tradecomp.select('hist')
    # print(df1)
