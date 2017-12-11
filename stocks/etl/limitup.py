import numpy as np
import pandas as pd

from stocks.gene import limitup
from stocks.data import _datautils

basics = _datautils.filter_basic(_datautils.get_basics())

codes = basics['code'].values
ups = limitup.get_limit_up(codes,start='2017-06-01')
ups.to_csv('../data/limitup.csv',encoding='utf-8')