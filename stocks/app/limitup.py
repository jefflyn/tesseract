import sys
from sys import argv

import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup

pd.set_option('display.width', 600)

if len(argv) < 2:
    print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
    sys.exit(0)
codes = argv[1]

code_list = codes.split(',')
print(code_list)

df = limitup.get_limit_up(code_list, start='2017-06-01')
print(df)
