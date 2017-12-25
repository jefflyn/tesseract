import sys
from sys import argv

import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import maup

pd.set_option('display.width',800)

if len(argv) < 2:
    print("Invalid args! At least 2 args like: python ma.py False | True ...")
    sys.exit(0)

isup = argv[1]

codes = []
if len(argv) == 3:
    codes = argv[2].split(',')
else:
    codes = _datautils.get_app_codes()

data = maup.get_ma(codes)
if isup == 'true':
    data = maup.get_ma_up(data)

if len(argv) == 3:
    print(data)
else:
    data.to_csv("../data/madata.csv", encoding='utf-8')
    _datautils.to_db(data, tbname='ma_data')