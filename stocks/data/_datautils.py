from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

import pymysql
from sqlalchemy import create_engine

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')

def get_app_codes():
    cf = get_data('./data/cf.txt', sep=' ')['code'].astype('str').str.zfill(6)
    # mo = get_data('./data/monitor.txt', sep=' ')['code'].astype('str').str.zfill(6)
    ot = get_data('./data/other.txt', sep=' ')['code'].astype('str').str.zfill(6)
    pa = get_data('./data/pa.txt', sep=' ')['code'].astype('str').str.zfill(6)
    tr = get_data('./data/trace.txt', sep=' ')['code'].astype('str').str.zfill(6)

    codes = list(cf) + list(ot) + list(pa) + list(tr)
    return codes


def get_k_data(code=None, start=None):
    hist_data = ts.get_k_data(code, start)  # one day delay issue, use realtime interface solved
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
    
def get_basics(code=None, excludeCyb=False):
    data = pd.read_csv("../data/basics.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    if excludeCyb:
        data = data[data['code'].str.get(0) != '3']
    if code != None:
        data = data[data.code == code]
    return data    

def get_subnew():
    data = pd.read_csv("../data/concepts/subnew.csv", encoding="gbk")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_wavex():
    data = pd.read_csv("../data/wavex.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_wavepa():
    data = pd.read_csv("../data/wavepa.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_bottom():
    try:
        data = pd.read_csv("../data/bottom.csv", encoding="utf-8")
        data['code'] = data['code'].astype('str').str.zfill(6)
        return data
    except:
        print('bottom file not found')
        return pd.DataFrame(columns=['code'])

def get_limitup():
    data = pd.read_csv("../data/limitup.csv", encoding="utf-8")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

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
def concept_filter():
    return concepts

#to_db(concepts,'concepts')
