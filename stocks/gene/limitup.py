from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import  _datautils

def get_today_limitup():
    todayquo = _datautils.get_totay_quotations()
    todayquo = todayquo[todayquo['p_change'] >= 9.9]
    return todayquo[['code', 'name', 'p_change']]

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
        hist_data = hist_data[['code', 'date', 'close', 'p_change', 'low']]
        hist_data = hist_data[hist_data['p_change'] >= 9.9] if up else hist_data[hist_data['p_change'] <= -9.9]
        # hist_data.reset_index()
        result = result.append(hist_data, ignore_index=True)
    endtime = datetime.datetime.now()
    print("total time: %ds" % (endtime - starttime).seconds)
    return result


"""
get limit up times by default 2 times in 90 days
"""
def count(df=None, times=None, condition=[90, 2]):
    if df.empty:
        return df
    dfgroup = df.groupby('code')
    codes = list(dfgroup.groups.keys())
    size = dfgroup.p_change.count()
    mindate = dfgroup.date.min()
    maxdate = dfgroup.date.max()
    low = dfgroup.low.last() #时间区间内最近涨停的最低价

    dfgroup = pd.DataFrame({'code': codes, 'count':size, 'mindate':mindate, 'maxdate':maxdate, 'lmtuplow':low})
    dfgroup = dfgroup.sort_values('count', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    if times != None:
        starttime = datetime.datetime.now()
        days = datetime.timedelta(-condition[0])
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        dfgroup = dfgroup[(dfgroup['count'] > times) | ((dfgroup['mindate'] >= start) & (dfgroup['count'] >= condition[1]))] # at least 2 times in 90d
    # names = [_datautils.get_basics(code).at[_datautils.get_basics(code).index.get_values()[0], 'name'] for code in codes]

    return dfgroup

def etl():
    basics = _datautils.filter_basic(_datautils.get_basics())
    codes = basics['code'].values

    ups = limitup.get_limit_up(codes)
    ups.to_csv('../data/tmp/limitupx.csv', encoding='utf-8')
    ups = limitup.count(ups)
    ups['code'] = ups.index
    #save to db
    _datautils.to_db(ups, 'limitupx')

if __name__ == '__main__':
    # lu = get_today_limitup()
    # print(lu)
    # exit()
    # from stocks.data import _datautils
    df = get_limit_up(['603388','600985', '600856','601908','600917'], start='2017-01-01')
    dfcount = (count(df, 1))
    print(df)
    print(dfcount)