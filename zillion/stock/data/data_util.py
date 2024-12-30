import datetime

import pandas as pd
import tushare as ts

from utils.datetime import date_util
from zillion.utils.db_util import read_query
from zillion.utils.db_util import read_sql

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')
yeardays = datetime.timedelta(days=-365)
oneyearago = (datetime.datetime.now() + yeardays).strftime('%Y%m%d')
oneweek = datetime.timedelta(days=-7)
weekago = (datetime.datetime.now() + oneweek).strftime('%Y%m%d')

INDEX_DICT = {'000001': '上证指数', '000016': '上证50', '000300': '沪深300',
              '399001': '深证成指', '399005': '中小板指', '399006': '创业板指'}
INDEX_LIST = ['000001.SH', '000300.SH', '000016.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399008.SZ']

basics = read_sql("select * from basics", params=None)


def get_issue_price():
    '''
    获取本地最早交易价格20100101后（发行价）
    :return:
    '''
    sql = 'select ht.trade_date,ht.code,ht.pre_close issue_price from hist_trade_day ht inner join ' \
          '(select code, min(trade_date) list_date from hist_trade_day group by code) hs ' \
          'on ht.code=hs.code and ht.trade_date=hs.list_date'
    df = read_query(sql)
    df.index = df['code']
    return df


def get_ma_data(code=None, trade_date=None):
    """
    获取移动平均数据
    :param code:
    :return:
    """
    sql = 'select * from hist_ma_day where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if trade_date is not None:
        sql += 'and trade_date = :trade_date '
    params = {'trade_date': trade_date, 'code': code}
    df = read_sql(sql, params=params)
    return df


def get_codes_by_wave(from_date='2019-01-01', pct_change=100):
    """
    选波段
    :return:
    """
    sql = "select distinct code from wave_data_2019 where begin >= :from_date and `change` >= :pct_change"
    params = {'from_date': from_date, 'pct_change': pct_change}
    df = read_sql(sql, params)
    return list(df['code'])


def get_codes_by_region(region=''):
    """
    查询省或市的stocks code
    :return:
    """
    sql = 'select code from basics where area like :region'
    params = {'region': '%' + region + '%'}
    df = read_sql(sql, params)
    return list(df['code'])


def get_normal_codes():
    """
    常规stocks code, 不含st和次新
    :return:
    """
    sql = 'select code from basics where name not like :st and list_date < :list_date'
    params = {'st': '%ST%', 'list_date': oneyearago}
    df = read_sql(sql, params)
    return list(df['code'])


def get_all_wave_data():
    """
    全部stocks wave
    :return:
    """
    sql = 'select * from select_wave_all'
    df = read_query(sql)
    return df


def get_normal_wave_data():
    """
    常规stocks wave
    :return:
    """
    sql = 'select * from select_wave_all where ' \
          'code in (select code from basics where name not like :st and list_date < :list_date)'
    params = {'st': '%ST%', 'list_date': oneyearago}
    df = read_sql(sql, params)
    return df


def get_subnew_wave_data():
    """
    次新stocks wave
    :return:
    """
    sql = 'select * from select_wave_all where code in (select code from basics where list_date >= :list_date)'
    params = {'list_date': oneyearago}
    df = read_sql(sql, params)
    return df


def get_st_wave_data():
    """
    st zillion wave
    :return:
    """
    sql = 'select * from select_wave_all where code in (select code from basics where name like :st)'
    params = {'st': '%ST%'}
    df = read_sql(sql, params)
    return df


def get_up_gap_codes(days=7):
    """
    获取时间范围内向上跳空的代码
    :param days:
    :return:
    """
    from_date = date_util.DATE_BEFORE_7_DAYS
    sql = 'select * from hist_trade_day where trade_date >=:fdate'
    params = {'fdate': from_date}
    df = read_sql(sql, params=params)
    group_df = df.groupby(df['code'])
    result_codes = []
    for code, group in group_df:
        # if code == '000531':
        #     print('')
        group = group.sort_values(['trade_date'], ascending=False)
        group_size = len(list(group['trade_date']))
        pre_low_arr = []
        next_low_arr = []
        for index in range(group_size - 1):
            pre_data = group.iloc[index + 1]
            next_data = group.iloc[index]

            pre_high = pre_data['high']
            pre_low = pre_data['low']
            pre_low_arr.append(pre_low)

            next_high = next_data['high']
            next_low = next_data['low']
            next_low_arr.append(next_low)
            if next_high < min(pre_low_arr):
                continue
            if min(next_low_arr) > pre_high:
                # print(pre_data)
                # print(next_data)
                result_codes.append(code)
    print('total size=' + str(len(result_codes)))
    print(result_codes)
    return result_codes


def get_codes_from_sql(sql=None):
    df = read_sql(sql, params=None)
    return list(df['code'])


def get_weekly(code=None, start=None, end=None):
    """
    获取历史周k
    :param code:
    :param start:
    :param end:
    :return:
    """
    sql = 'select * from hist_weekly where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '
    params = {'code': code, 'start': start, 'end': end}
    df = read_sql(sql, params=params)
    return df


def get_hist_week(code=None, n=None, start=None, end=None):
    """
    获取历史周k
    :param code:
    :param n:
    :param start:
    :param end:
    :return:
    """
    table_name = 'hist_weekly'
    sql = 'select * from ' + table_name + ' where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '
    if n is not None:
        sql += 'order by trade_date desc limit :n '
    params = {'code': code, 'start': start, 'end': end, 'n': n}
    df = read_sql(sql, params=params)
    df2 = df.reset_index(drop=True)
    return df2


def get_hist_trade_high_low(code=None, start=None, end=None):
    """
    获取历史日k high low
    :param code:
    :param start:
    :param end:
    :return:
    """
    table_name = 'hist_trade_day'
    sql = 'select code, max(high) as high, min(low) as low from ' + table_name + ' where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '
    sql += 'group by code'
    params = {'code': code, 'start': start, 'end': end}
    df = read_sql(sql, params=params)
    return df


def get_hist_trade(code=None, is_index=False, start=None, end=None, is_limit=False):
    """
    获取历史日k
    :param code:
    :param is_index:
    :param start:
    :param end:
    :param is_limit:
    :return:
    """
    table_name = 'hist_trade_day' if is_index is False else 'index_hist_k'
    sql = 'select * from ' + table_name + ' where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '
    if is_limit:
        sql += "and code not like '688%' and (close = round(pre_close * 1.1, 2)  or pct_change > 9.9) "
    params = {'code': code, 'start': start, 'end': end}
    df = read_sql(sql, params=params)
    return df


def get_pre_hist_trade(code, trade_date, is_index=False):
    """
    获取历史日k
    :param code: str
    :param trade_date: str
    :param is_index: boolean
    :return:
    """
    table_name = 'hist_trade_day' if is_index is False else 'hist_index_day'
    sql = 'select * from ' + table_name + ' where 1=1 '
    if isinstance(code, str):
        codes = list()
        codes.append(code)
        code = codes
        sql += 'and code in :code '
    sql += 'and trade_date <:trade_date '
    sql += 'order by trade_date desc limit 1 '
    params = {'code': code, 'trade_date': trade_date}
    # logs.info(sql + ' ' + str(params))
    df = read_sql(sql, params=params)
    return df


def get_monitor_stocks():
    df = read_query('select * from monitor_pool where is_valid=1')
    return df


def get_app_codes():
    df = get_my_stock_pool()
    codes = list(df['code'])
    return codes


def get_limitup_code(period_type='m', period='2019-01', times=3):
    sql = 'select distinct code from limitup_stat where period_type=:type and period=:period and times>=:times'
    params = {'type': period_type, 'period': period, 'times': times}
    df = read_sql(sql, params=params)
    return df


def get_ma_code(grade='a'):
    sql = 'select distinct b.code from hist_ma_day m join basics b on m.ts_code = b.ts_code where rank=:grade'
    params = {'grade': grade}
    df = read_sql(sql, params=params)
    return df


def get_my_stock_pool(type=None, hold=1):
    if type in ['combo', 'map', 'new']:
        sql = 'select * from select_x where 1=1 and on_target=1 and select_type=:select_type'
        params = {'select_type': type}
        df = read_sql(sql, params)
        if df is not None and df.empty is False:
            df['cost'] = None
            df['share'] = 100
            df['bottom'] = df['fire_price']
        return df
    else:
        sql = 'select * from my_stock_pool where 1=1 and is_hold=:hold'
        if hold is None:
            hold = 1
        params = {'hold': hold}
        if type is not None:
            params['type'] = type
            sql = sql + ' and platform=:type'
        df = read_sql(sql, params=params)
        return df


def get_code_by_concept(name=''):
    name_str = '%' + name + '%'
    params = {'name': name_str}
    sql = 'select distinct d.code, c.name from concept c ' \
          'inner join concept_detail d on c.code = d.concept_code ' \
          'where c.name like :name'
    df = read_sql(sql, params=params)
    codes = list(df['code'])
    concepts = set(df['name'])
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


def get_k_data(code=None, start=None, end=None):
    hist_data = ts.get_k_data(code, start, end)  # one day delay issue, use realtime interface solved
    if hist_data is None or len(hist_data) == 0:
        print(code + ' k data not found')
        return None
    try:
        latestdate = hist_data.tail(1).at[hist_data.tail(1).index.to_numpy()[0], 'date']
        if todaystr != latestdate:
            # get today data from [get_realtime_quotes(code)]
            realtime = ts.get_realtime_quotes(code)
            rt_date = realtime.at[0, 'date']
            if latestdate == rt_date:
                return hist_data
            # ridx = realtime.index.to_numpy()[0]
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


def filter_basic(_basics=None, cyb=True, before=None):
    # filter unused code
    if cyb is False:
        _basics = _basics[_basics['code'].str.get(0) != '3']
    if before is not None:
        _basics = _basics[(_basics['list_date'] > 0) & (_basics['list_date'] <= before)]
    # else:
    #     before = date_const.DATE_BEFORE_7_DAYS_SIMP
    #     _basics = _basics[(_basics['list_date'] > 0) & (_basics['list_date'] <= int(before))]
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


def get_last_trade_data(codes=None):
    """
    获取最近的一条交易数据
    :param codes:
    :return:
    """
    sql = 'select a.* from hist_trade_day a inner join ' \
          '(select code, max(trade_date) last_date from hist_trade_day group by code) b ' \
          'on a.code=b.code and a.trade_date = b.last_date ' \
          'where 1=1 '
    if codes is not None:
        if isinstance(codes, str):
            code_list = list()
            code_list.append(codes)
            codes = code_list
        sql += 'and a.code in :code '
    else:
        return None
    params = {'code': codes}
    df = read_sql(sql, params=params)
    df.index = df['code'].astype('str').str.zfill(6)
    return df


if __name__ == '__main__':
    # get_up_gap_codes()
    # k_data = ts.get_k_data('', ktype='W')
    # print(k_data)
    # print(format_amount(''))
    # print(format_amount(None))
    # print(format_amount(12.23))
    # print(format_amount(12.2389999989))
    # print(format_amount(1236))
    # print(format_amount(32589))
    # print(format_amount(325862))
    # print(format_amount(2369852))
    # print(format_amount(25896325))
    # print(format_amount(369852369))
    # print(get_last_trade_data(['', '']))
    df = get_data("id.csv")
    step = 28000
    for i in range(0, df.index.size, step):
        print(i, 1 + step)

    # df.to_csv("2_udate.sql")

