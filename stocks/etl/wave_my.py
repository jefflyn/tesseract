import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.gene import period

filePath = "../app/data/cf.txt"
mystk = pd.read_csv(filePath, sep=' ')

mystk['code'] = mystk['code'].astype('str').str.zfill(6)
codes = list(mystk['code'])
mywavedata = period.get_wave(codes, start='2016-01-04')

mywavedata.to_csv("../data/wavecf.csv",encoding='utf-8')

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
mywavedata.to_sql(name = 'wave_data_cf',con = engine,if_exists = 'replace',index = False,index_label = False)