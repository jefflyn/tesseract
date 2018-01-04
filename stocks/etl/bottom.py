import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.gene import period
from stocks.gene import bargain
from stocks.data import _datautils

# processing...
datadf = _datautils.get_data(filepath='../data/app/other.txt', sep=' ')
codes = list(datadf['code'])

wavedf = period.get_wave(codes)
df = bargain.get_bottom(wavedf)

df.to_csv("../data/bottom.csv",encoding='utf-8')
_datautils.to_db(df, 'bottom')
