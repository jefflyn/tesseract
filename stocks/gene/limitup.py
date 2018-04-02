from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import  _datautils

trade = pd.HDFStore('../data/trade.h5', complevel=9, complib='blosc')
histlimitup = trade.get('k_limitup_hist')

LIMITUP_MIN = 9.9
LIMITUP_MAX = 10.9
LIMITUP_FROM_DAYS = -365


def get_today_limitup():
    todayquo = _datautils.get_totay_quotations()
    todayquo = todayquo[todayquo['p_change'] >= LIMITUP_MIN]
    return todayquo[['code', 'name', 'p_change']]


"""
limitup default in one year 
start: YYYY-MM-DD
"""
def get_limitup_data(codes = None, isNature = True, start = None, end = None):
    starttime = datetime.datetime.now()
    if start == None:
        days = datetime.timedelta(LIMITUP_FROM_DAYS)
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')

    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    limitupdf = histlimitup[histlimitup.code.isin(code_list)]
    limitupdf = limitupdf[limitupdf.date >= start]
    if end is not None:
        limitupdf = limitupdf[limitupdf.date <= end]
    if isNature:
        limitupdf = limitupdf[(limitupdf.p_change <= LIMITUP_MAX) & (limitupdf.high > limitupdf.low)]

    return limitupdf

"""
Deprecated
limitup default in one year 
start: YYYY-MM-DD
"""
def get_limit_up(codes = None, start = None, end = None, up = True):
    # print("get limitups... ")
    starttime = datetime.datetime.now()
    if start == None:
        days = datetime.timedelta(LIMITUP_FROM_DAYS)
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    result = pd.DataFrame()
    for code in code_list:
        hist_data = ts.get_hist_data(code, start, end)
        hist_k = ts.get_k_data(code, start, end)
        if hist_data is None or len(hist_data) == 0:
            continue
        hist_data.insert(0, 'date', hist_data.index)
        hist_data.insert(1, 'code', code)
        hist_data = hist_data[['code', 'date', 'close', 'p_change', 'low']]
        hist_data = hist_data[hist_data['p_change'] >= LIMITUP_MIN] if up else hist_data[hist_data['p_change'] <= -LIMITUP_MIN]
        # hist_data.reset_index()
        result = result.append(hist_data, ignore_index=True)
    endtime = datetime.datetime.now()
    # print("total time: %ds" % (endtime - starttime).seconds)
    return result


"""
get limit up times by default 2 times in 90 days
"""
def count(df=None):
    if df.empty:
        return df

    count_data_list = []
    # group by data
    dfgroup = df.groupby('code')
    for name, group in dfgroup:
        count_data = []
        starttime = datetime.datetime.now()
        days = datetime.timedelta(-30)
        start30 = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        lupdf = group[group.date >= start30]
        count_30d = lupdf.iloc[:, 0].size

        days = datetime.timedelta(-90)
        qrt1st = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        lupdf = group[(group.date >= qrt1st) & (group.date < start30)]
        count_qrt1st = lupdf.iloc[:, 0].size

        days = datetime.timedelta(-180)
        qrt2nd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        lupdf = group[(group.date >= qrt2nd) & (group.date < qrt1st)]
        count_qrt2nd = lupdf.iloc[:, 0].size

        days = datetime.timedelta(-270)
        qrt3rd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        lupdf = group[(group.date >= qrt3rd) & (group.date < qrt2nd)]
        count_qrt3rd = lupdf.iloc[:, 0].size

        lupdf = group[group.date < qrt3rd]
        count_qrt4th = lupdf.iloc[:, 0].size

        size = group.p_change.count()
        mindate = group.date.min()
        maxdate = group.date.max()
        low = group.low.min() #the low in time limitup time zone
        high = group.high.max()

        count_data.append(name)
        count_data.append(size)
        count_data.append(count_30d)
        count_data.append(count_qrt1st)
        count_data.append(count_qrt2nd)
        count_data.append(count_qrt3rd)
        count_data.append(count_qrt4th)
        count_data.append(mindate)
        count_data.append(maxdate)
        count_data.append(round(low, 2))
        count_data.append(round(high, 2))
        count_data_list.append(count_data)

    count_result = pd.DataFrame(data=count_data_list,
        columns=['code', 'count', 'count_30d', 'count_q1', 'count_q2', 'count_q3', 'count_q4', 'mindate', 'maxdate',
                 'lup_low', 'lup_high'])
    count_result = count_result.sort_values('count', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')

    return count_result

if __name__ == '__main__':
    # lu = get_today_limitup()
    # print(lu)
    # exit()
    # from stocks.data import _datautils
    df = get_limitup_data(['600831','000710'])
    dfcount = count(df)

    print(df)
    print(dfcount)