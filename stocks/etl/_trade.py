from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts


from stocks.data import _datautils as dt

basics = dt.filter_basic(dt.get_basics())
codes = basics['code'].values

