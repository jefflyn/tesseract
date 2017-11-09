import tushare as ts
import numpy as np
import pandas as pd

basics = ts.get_stock_basics()
basics['code'] = basics['code'].astype('str').str.zfill(6)

basics.to_csv("./data/basics.csv")