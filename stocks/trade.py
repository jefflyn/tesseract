from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

pd.set_option('display.width', 600)

# hist = ts.get_hist_data('002415',start='2017-05-15')
# print(hist.tail(10))

h = ts.get_h_data('002415',start='2017-05-15')
dateindex = (h.tail(1).index.get_values()[0])
dateindex = datetime.datetime.utcfromtimestamp(dateindex.astype('O')/1e9)
print(dateindex.strftime("%Y-%m-%d"))
print(h.tail(10))

# k = ts.get_k_data('002415',start='2017-05-15')
# print(k.head(10))