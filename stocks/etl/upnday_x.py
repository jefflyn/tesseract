import numpy as np
import pandas as pd

from stocks.gene import upnday
from stocks.data import _datautils

#x = _datautils.get_subnew()
x = _datautils.get_basics_fromh5()
#x = x[(x.timeToMarket>=20170901) & (x.timeToMarket<=20171214)]

# x = _datautils.get_limitup()
# x = x[['code']].drop_duplicates()

# x = _datautils.get_data('../data/concepts/ai.csv')
# x = _datautils.filter_cyb(x)

# processing...
codes = list(x['code'])
xdata = upnday.get_upnday(codes)

xdata.to_csv("../data/upndayx.csv",encoding='utf-8')
_datautils.to_db(xdata, tbname='upnday')