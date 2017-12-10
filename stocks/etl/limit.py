import numpy as np
import pandas as pd

from stocks.gene import limitup
from stocks.data import _datautils

basics = pd.read_csv("../data/basics.csv", encoding='gbk')
basics['code'] = basics['code'].astype('str').str.zfill(6)

basics = _datautils.filter_basic(basics)

codes = basics['code'].values
ups = limitup.get_limit_up(codes,start='2017-07-01')
ups.to_csv("../data/limitup.csv")