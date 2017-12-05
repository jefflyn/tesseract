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
        hist_data = ts.get_k_data(code, start='2016-11-19')
        if hist_data is None or len(hist_data) == 0:
            continue
        hist_data.insert(0, 'date', hist_data.index)
        hist_data.insert(1, 'code', code)
        hist_data = hist_data[['code','date','p_change']]
        hist_data = hist_data[hist_data['p_change'] >= 9.9] if up else hist_data[hist_data['p_change'] <= -9.9]
        # hist_data.reset_index()
        result = result.append(hist_data, ignore_index = True)
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
    return result
