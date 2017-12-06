import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.etl import utils
from stocks.gene import limitup
from stocks.gene import period

basics = pd.read_csv("../data/basics.csv", encoding='gbk')
basics['code'] = basics['code'].astype('str').str.zfill(6)

basics = utils.basic_filter(basics, before=20170901)

codes = basics['code'].values

wavedata = period.get_wave(codes, start='2016-01-04')
wavedata.to_csv("../data/wavedata.csv")

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
wavedata.to_sql(name = 'wave_data',con = engine,if_exists = 'replace',index = False,index_label = False)