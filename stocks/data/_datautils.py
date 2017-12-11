import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine


def get_data(filepath=None, encoding='gbk'):
    data = pd.read_csv(filepath, encoding=encoding)
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_basics():
    data = pd.read_csv("../data/basics.csv", encoding="gbk")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_subnew():
    data = pd.read_csv("../data/concepts/subnew.csv", encoding="gbk")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_wavex():
    data = pd.read_csv("../data/wavex.csv", encoding="gbk")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_wavepa():
    data = pd.read_csv("../data/wavepa.csv", encoding="gbk")
    data['code'] = data['code'].astype('str').str.zfill(6)
    return data

def get_buttom():
    data = pd.read_csv("../data/bottom.csv", encoding="gbk")
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
