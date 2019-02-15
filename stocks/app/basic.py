import sys
from sys import argv
import pandas as pd

import tushare as ts
from stocks.data import data_util

pd.set_option('display.width', 800)
pd.set_option('precision', 3)

if len(argv) < 2:
    print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
    sys.exit(0)
codes = argv[1]

codelist = codes.split(',')
df = data_util.get_basics()
df = df[df.code.isin(codelist)]
print(df)