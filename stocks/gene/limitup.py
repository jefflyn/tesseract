from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

# all 1 year takes about 330s
def get_limit_up(codes = None, start = None, end = None, up = True):
    print("get limitups... ")
    starttime = datetime.datetime.now()
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    result = pd.DataFrame()
    for code in code_list:
        hist_data = ts.get_hist_data(code, start, end)
        if hist_data is None or len(hist_data) == 0:
            continue
        hist_data.insert(0, 'date', hist_data.index)
        hist_data.insert(1, 'code', code)
        hist_data = hist_data[['code', 'date', 'close', 'p_change']]
        hist_data = hist_data[hist_data['p_change'] >= 9.9] if up else hist_data[hist_data['p_change'] <= -9.9]
        # hist_data.reset_index()
        result = result.append(hist_data, ignore_index=True)
    endtime = datetime.datetime.now()
    print("total time: %ds" % (endtime - starttime).seconds)
    return result

def count(df=None):
    if df.empty:
        return df

    df = df[df['p_change'] >= 9.9]
    # dfgroup = df.groupby("code")['p_change'].count()
    dfgroup = df.groupby("code").agg({'p_change': np.size})
    dfgroup = dfgroup.sort_values('p_change', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return dfgroup

#from stocks.data import _datautils
# print(count(_datautils.get_limitup()))
# df = get_limit_up('002620',start='2017-01-01')
# print(df)