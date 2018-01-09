from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import  _datautils

# all 1 year
def get_limit_up(codes = None, start = None, end = None, up = True):
    print("get limitups... ")
    starttime = datetime.datetime.now()
    if start == None:
        days = datetime.timedelta(-365)
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
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

def count(df=None, times=None):
    if df.empty:
        return df
    df = df[df['p_change'] >= 9.9]
    # dfgroup = df.groupby("code")['p_change'].count()
    dfgroup = df.groupby("code").agg({'p_change': np.size, 'date': np.min})
    dfgroup.rename(columns={'p_change': 'count'}, inplace=True)
    dfgroup = dfgroup.sort_values('count', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    if times != None:
        starttime = datetime.datetime.now()
        days = datetime.timedelta(-90)
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        dfgroup = dfgroup[(dfgroup['count'] > times) | ((dfgroup['date'] >= start) & (dfgroup['count'] > 1))] # at least 2 times in 90d
    codes = list(dfgroup.index.get_values())
    names = [_datautils.get_basics(code).at[_datautils.get_basics(code).index.get_values()[0], 'name'] for code in codes]
    dfgroup['name'] = names
    return dfgroup

if __name__ == '__main__':
    # from stocks.data import _datautils
    df = get_limit_up(['002907','600985', '600856','601908','600917'], start='2017-01-01')
    dfcount = (count(df, 1))
    print(df)
    print(dfcount)