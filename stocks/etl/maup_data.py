import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import maup

# filePath = "../app/data/pa.txt"
# mystk = pd.read_csv(filePath, sep=' ')
# mystk['code'] = mystk['code'].astype('str').str.zfill(6)
# codes = list(mystk['code'])

basics = _datautils.filter_basic(_datautils.get_basics())
codes = basics['code'].values

data = maup.get_ma(codes)
# data = maup.get_ma_up(data)

data.to_csv("../data/madata.csv",encoding='utf-8')

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
data.to_sql(name='ma_data', con=engine, if_exists='replace', index=False, index_label=False)