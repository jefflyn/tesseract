import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as _dt

trade = pd.HDFStore('trade.h5')
tradecomp = pd.HDFStore('trade_comp.h5', complevel=9, complib='blosc')

oneday = dt.timedelta(-1)
today = datetime.today()# + oneday
todaystr = datetime.strftime(today, '%Y-%m-%d')
print(todaystr)
i = 0
while todaystr > '2017-06-13':
    try:
        i = i + 1
        print(i)
        todaydf = _dt.get_totay_quotations(todaystr)
        size = len(todaydf.index.get_values())
        dates = [todaystr] * size
        todaydf.insert(0,'date',dates)
        print(size)
        trade.append('hist', todaydf)
        tradecomp.append('hist', todaydf)
    except Exception as e:
        print(str(e))
    today = today + oneday
    todaystr = datetime.strftime(today, '%Y-%m-%d')
    print(todaystr)

trade.close()
tradecomp.close()
