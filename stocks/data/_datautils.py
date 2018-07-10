from datetime import date
import datetime
import numpy as np
import pandas as pd

import tushare as ts

import pymysql
from sqlalchemy import create_engine

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')
yeardays = datetime.timedelta(days=-365)
oneyearago = (datetime.datetime.now() + yeardays).strftime('%Y%m%d')
oneweek = datetime.timedelta(days=-7)
weekago = (datetime.datetime.now() + oneweek).strftime('%Y%m%d')

INDEX_DICT = {'000001': '上证指数', '000016': '上证50', '000300': '沪深300',
              '399001': '深证成指', '399005': '中小板指', '399006': '创业板指'}


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



"""
marketTimeFrom: yyyymmdd
"""
def get_subnew(cyb = False, marketTimeFrom = None):
    if marketTimeFrom == None:
        marketTimeFrom = oneyearago
    basics = get_basics_fromh5(excludeCyb=cyb)
    # filter unused code
    if cyb is False:
        basics = basics[basics['code'].str.get(0) != '3']
    basics = basics[(basics.timeToMarket >= int(marketTimeFrom)) & (basics.timeToMarket < int(weekago))]
    return basics


def format_percent(df=None, columns=[], precision=2):
    if df == None:
        return None
    for columm in columns:
        df[columm] = df[columm].apply(lambda x: str(round(x, precision)) + '%')


"""
"""
def get_latest_h5(code=None, excludeCyb=False):
    trade = pd.HDFStore('../data/trade.h5')
    data = trade['latest']
    if excludeCyb:
        data = data[data['code'].str.get(0) != '3']
    if code != None:
        data = data[data.code == code]
    trade.close()
    return data


def get_sz50():
    sz50df = ts.get_sz50s()
    return list(sz50df['code'])


def get_totay_quotations(datestr=None):
    return ts.get_day_all(date=datestr)


def get_app_codes():
    pa = get_data('../data/app/pa.txt', sep=' ')['code'].astype('str').str.zfill(6)
    cf = get_data('../data/app/cf.txt', sep=' ')['code'].astype('str').str.zfill(6)
    ot =[] #get_data('../data/app/other.txt', sep=' ')['code'].astype('str').str.zfill(6)
    codes = list(pa) + list(cf) + list(ot)
    return codes

def get_ot_codes():
    ot = get_data('../data/app/other.txt', sep=' ')['code'].astype('str').str.zfill(6)
    codes = list(ot)
    return codes


def get_monitor_codes(flag=None):
    codes = None
    if flag == 'ot':
        ot = get_data('../data/app/monitorot.txt', sep=' ')['code'].astype('str').str.zfill(6)
        codes = list(ot)
    elif flag == 'my':
        my = get_data('../data/app/monitormy.txt', sep=' ')['code'].astype('str').str.zfill(6)
        codes = list(my)
    elif flag == 'x':
        my = get_data('../data/app/monitorx.txt', sep=' ')['code'].astype('str').str.zfill(6)
        codes = list(my)
    return codes


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
                newone = {'date': todaystr, 'open': float(realtime.at[0, 'open']), 'close': float(realtime.at[0, 'price']),
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


def get_basics_fromh5(code=None, excludeCyb=False):
    fundamental = pd.HDFStore('../data/fundamental.h5')
    data = fundamental['basics']
    if excludeCyb:
        data = data[data['code'].str.get(0) != '3']
    if code != None:
        data = data[data.code == code]
    fundamental.close()
    return data

"""
index: code
"""
def get_basics(code=None, excludeCyb=False, index=False, before=None):
    if index == True:
        return INDEX_DICT[code]

    data = pd.read_csv("../data/basics.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)

    data = filter_basic(basics=data, excludeCyb=excludeCyb, before=before)

    if code != None:
        data = data[data.code == code]
    data.index = list(data['code'])
    return data


def get_hist_k(ktype=None):
    """
    hist k data
    :return: 
    """
    data = None
    if ktype == 'W':
        data = pd.read_csv("../data/hist_k_week.csv", encoding="utf-8")
    elif ktype == 'M':
        data = pd.read_csv("../data/hist_k_month.csv", encoding="utf-8")
    else:
        data = pd.read_csv("../data/hist_k_day.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data


def get_bottom():
    try:
        data = pd.read_csv("../data/bottom.csv", encoding="utf-8")
        data['code'] = data['code'].astype('str').str.zfill(6)
        return data
    except:
        print('bottom file not found, return empty code list.')
        return pd.DataFrame(columns=['code'])

#save to db
def to_db(data, tbname=None):
    engine = create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stocks?charset=utf8")
    data.to_sql(name=tbname, con=engine, if_exists='replace', index=False, index_label=False)

#filter cyb
def filter_cyb(datadf):
    datadf = datadf[datadf['code'].str.get(0) != '3']
    return datadf

##
def filter_basic(basics, excludeCyb = False, before = 20170701):
    # filter unused code
    if excludeCyb is True :
        basics = basics[basics['code'].str.get(0) != '3']
    if before is not None:
        basics = basics[(basics['timeToMarket'] > 0) & (basics['timeToMarket'] <= before)]
    return basics



def get_stock_data(type='i', filename=None, encoding='gbk', sep='\t', excludeCyb=True):
    path = ''
    if type == 'i':
        path = '../data/industry/' + filename
    else:
        path = '../data/concept/' + filename
    data = None
    try:
        # file = open(path)
        data = pd.read_csv(path, sep=sep, encoding=encoding)
    except:
        file = open(path)
        data = pd.read_csv(file, sep=sep, encoding='utf-8')

    data['code'] = data['code'].apply(lambda code : code[2:])

    # data['code'] = data['code'].astype('str').str.zfill(6)
    if excludeCyb:
        data = data[data['code'].str.get(0) != '3']
    return data


def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False


def format_amount(amount=None):
    if isnumber(amount) == False:
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
        result = round(amount / (10000*10000), 1)
        return str(result) + '亿'


if __name__ == '__main__':
    k_data = ts.get_k_data('000836',ktype='W')
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