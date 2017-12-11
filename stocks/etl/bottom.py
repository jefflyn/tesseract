import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.gene import period
from stocks.gene import bargain
from stocks.data import _datautils

# processing...
df = bargain.get_bottom(_datautils.get_wavex())

df.to_csv("../data/bottom.csv",encoding='utf-8')

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
df.to_sql(name = 'bottom',con = engine,if_exists = 'replace',index = False,index_label = False)