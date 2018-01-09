import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.data import _datautils

basics = _datautils.filter_basic(_datautils.get_basics())
codes = basics['code'].values

# x = _datautils.get_data('../data/concepts/hainan.csv')
# codes = list(x['code'])

ups = limitup.get_limit_up(codes)
ups.to_csv('../data/limitup.csv', encoding='utf-8')
ups = limitup.count(ups)
ups['code'] = ups.index

#save to db
_datautils.to_db(ups, 'limitupx')
