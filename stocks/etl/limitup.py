import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.data import _datautils
#
# basics = _datautils.filter_basic(_datautils.get_basics())
# codes = basics['code'].values
# ups = limitup.get_limit_up(codes, start='2017-01-01')
# ups.to_csv('../data/limitup.csv', encoding='utf-8')

x = _datautils.get_data('../data/concepts/hainan.csv')
codes = list(x['code'])
ups = limitup.get_limit_up(codes, start='2017-06-01')
# ups.to_csv('../data/limitup.csv', encoding='utf-8')
ups = limitup.count(ups)
ups['code'] = ups.index

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
ups.to_sql(name='limitup_x', con=engine, if_exists='replace', index=False, index_label=False)