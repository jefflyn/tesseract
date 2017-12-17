import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.gene import period
from stocks.data import _datautils

# x = _datautils.get_subnew()

x = _datautils.get_limitup()
x = x[['code']].drop_duplicates()

x = _datautils.get_data('../data/concepts/ai.csv')
x = _datautils.filter_cyb(x)

# processing...
codes = list(x['code'])
xdata = period.get_wave(codes, start='2016-01-04')

xdata.to_csv("../data/wavex.csv",encoding='utf-8')

#save to db
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
xdata.to_sql(name='wave_data_x', con=engine, if_exists='replace', index=False, index_label=False)