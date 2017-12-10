import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

def get_concept_subnew():
    concept_subnew = pd.read_csv("../data/concepts/subnew.csv", encoding='gbk')
    concept_subnew['code'] = concept_subnew['code'].astype('str').str.zfill(6)
    return concept_subnew

get_concept_subnew()

def get_concepts():
    concepts = pd.read_csv("../data/concepts.csv", encoding='gbk')
    concepts['code'] = concepts['code'].astype('str').str.zfill(6)
    return concepts

def get_basics():
    basics = pd.read_csv("../data/basics.csv", encoding='gbk')
    basics['code'] = basics['code'].astype('str').str.zfill(6)
    return basics

def filter_cyb(datadf):
    datadf = datadf[datadf['code'].str.get(0) != '3']
    return datadf

def filter_cyb(datadf):
    datadf = datadf[datadf['code'].str.get(0) != '3']
    return datadf

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
