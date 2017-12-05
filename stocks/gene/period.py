from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

def get_limit_up(codes = None, start = None, end = None):
    starttime = datetime.datetime.now()
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else: code_list = codes

    result = pd.DataFrame()
    for code in code_list:
        hist_data = ts.get_k_data(code, start='2016-12-01')
        if hist_data is None or len(hist_data) == 0:
            continue
        min_rec = hist_data.min()['low']
        latest = hist_data.tail(1)
        idx = latest.index.get_values()[0]
        latest_date_str = latest.at[idx, 'date']
        latest_date = datetime.datetime.strptime(latest_date_str, '%Y-%m-%d')
        delta = starttime - latest_date

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
    return result
