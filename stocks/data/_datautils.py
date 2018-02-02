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

INDEX_DICT = {'000001': '上证指数', '000016': '上证50', '000300': '沪深300',
              '399001': '深证成指', '399005': '中小板指', '399006': '创业板指'}

def get_subnew(cyb = False):
    basics = get_basics_fromh5(excludeCyb=cyb)
    # filter unused code
    if cyb is False:
        basics = basics[basics['code'].str.get(0) != '3']
    basics = basics[(basics['timeToMarket'] >= int(oneyearago))]
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
    ot = get_data('../data/app/other.txt', sep=' ')['code'].astype('str').str.zfill(6)
    tr = get_data('../data/app/trace.txt', sep=' ')['code'].astype('str').str.zfill(6)
    codes = list(cf) + list(ot) + list(pa) + list(tr)
    return codes


def get_monitor_codes():
    my = get_data('../data/app/monitormy.txt', sep=' ')['code'].astype('str').str.zfill(6)
    ot = get_data('../data/app/monitorot.txt', sep=' ')['code'].astype('str').str.zfill(6)
    codes = list(my) + list(ot)
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

def get_basics(code=None):
    data = pd.read_csv("../data/basics.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    if code != None:
        data = data[data.code == code]
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

def get_basics(code=None, excludeCyb=False, index=False):
    if index == True:
        return INDEX_DICT[code]

    data = pd.read_csv("../data/basics.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    if excludeCyb:
        data = data[data['code'].str.get(0) != '3']
    if code != None:
        data = data[data.code == code]
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
    db_con = pymysql.connect(
        user = 'linjingu',
        password = 'linjingu',
        port = 3306,
        host = 'localhost',
        db = 'stocks',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
    )
    engine = create_engine("mysql+pymysql://linjingu:linjingu@localhost:3306/stocks?charset=utf8")
    data.to_sql(name = tbname,con = engine,if_exists = 'replace',index = False,index_label = False)

#filter cyb
def filter_cyb(datadf):
    datadf = datadf[datadf['code'].str.get(0) != '3']
    return datadf

##
def filter_basic(basics, cyb = False, before = 20170701):
    # filter unused code
    if cyb is False :
        basics = basics[basics['code'].str.get(0) != '3']
    if before is not None:
        basics = basics[(basics['timeToMarket'] > 0) & (basics['timeToMarket'] <= before)]
    return basics

##
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