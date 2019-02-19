import sys
from sys import argv

import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine
import stocks.base.db_util as _dt
from stocks.gene import limitup
from stocks.gene import maup

pd.set_option('display.width',800)

if len(argv) < 3:
    print("Invalid args! At least 2 args like: python ma.py code y | n ...")
    sys.exit(0)

isup = argv[2]

codes = []
if len(argv) == 3:
    codes = argv[1].split(',')
else:
    codes = _datautils.get_app_codes()

data = maup.get_ma(codes)
if isup == 'y':
    data = maup.get_ma_up(data)

if len(argv) == 3:
    print(data)
else:
    data.to_csv("../data/madata.csv", encoding='utf-8')
    _dt.to_db(data, tbname='ma_data')