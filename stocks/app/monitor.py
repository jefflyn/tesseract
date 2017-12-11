import os
import pandas as pd

import tushare as ts
from stocks.app import falco
from stocks.data import _datautils

pd.set_option('display.width', 600)
pd.set_option('precision', 3)

df = _datautils.get_subnew()
# codes = list(df['code'])
# falco.monitor(codes)