from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

pd.set_option('display.width', 600)

def get_wave(codes=None, start='2016-01-04', end=None, beginlow=True, duration=0, pchange=0):
    starttime = datetime.datetime.now()
    print("get wave start at [%s]" % starttime)
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else: code_list = codes

    perioddf_list = []
    for code in code_list:
        print("   >>> processing %s ..." % code)
        hist_data = ts.get_k_data(code, start) #one day delay issue
        # hist_data = ts.get_h_data(code, start)  # network issue
        if hist_data is None or len(hist_data) == 0:
            continue
        left_data = wavefrom(code, hist_data, beginlow, 'left', duration, pchange)
        right_data = wavefrom(code, hist_data, beginlow, 'right', duration, pchange)
        period_df = pd.DataFrame(left_data + right_data,columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'p_change'])
        perioddf_list.append(period_df)
        print("   >>> done!")

    if perioddf_list is None or len(perioddf_list) == 0:
        return 'result is empty, please check the code is exist!'
    result = pd.concat(perioddf_list, ignore_index=True)
    result = result.sort_values(by=['code','begin'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    # pd.set_option('display.width', 600)
    # print(result)

    endtime = datetime.datetime.now()
    print("get wave finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return result

def wavefrom(code, df, beginlow, direction='left', duration=0, pchange=0):
    period_data = []
    # for get_k_data use
    firstdate = df.head(1).at[df.head(1).index.get_values()[0],'date']
    lastdate = df.tail(1).at[df.tail(1).index.get_values()[0], 'date']
    # firstdate = datetime.datetime.utcfromtimestamp((df.tail(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")
    # lastdate = datetime.datetime.utcfromtimestamp((df.head(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")

    # start from the lowest price, find the wave from both sides
    pivot_low = df.min()['low']
    pivot_rec = df[df.low == pivot_low]
    # print(pivot_rec)
    pivot_index = pivot_rec.index.get_values()[0]
    pivot_date = pivot_rec.at[pivot_index, 'date']
    # pivot_date = datetime.datetime.utcfromtimestamp((pivot_rec.tail(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")
    pivot_close = pivot_rec.at[pivot_index, 'close']

    ismax = beginlow
    begindate = firstdate
    enddate = pivot_date
    beginprice = pivot_low
    endprice = pivot_low

    if direction == 'right':
        begindate = pivot_date
        enddate = lastdate
    diff_days = datetime.datetime.strptime(enddate, '%Y-%m-%d') - datetime.datetime.strptime(begindate, '%Y-%m-%d')

    while diff_days.days > duration:
        data = df[(df.date >= begindate) & (df.date < enddate)] if direction == 'left' else df[(df.date > begindate) & (df.date <= enddate)]
        price = data.max()['high'] if ismax else data.min()['low']

        status = ''
        rec = data[data.high == price] if ismax else data[data.low == price]
        idx = rec.index.get_values()[0]
        date = rec.at[idx, 'date']
        close = rec.at[idx, 'close']

        if direction == 'left':
            beginprice = price
            begindate = date
            status = 'down' if ismax else 'up'
        if direction == 'right':
            #if the latest one, get the close price, calculate the actual rises
            endprice = close if date == lastdate else price
            enddate = date
            status = 'up' if ismax else 'down'

        diff_precent = (endprice - beginprice) / beginprice * 100
        if abs(diff_precent) < pchange:
            break
        list = []
        # ['code', 'begin', 'end', 'status' 'begin_price', 'end_price', 'days', 'p_change']
        list.append(code)
        list.append(begindate)
        list.append(enddate)
        list.append(status)
        list.append(beginprice)
        list.append(endprice)
        list.append((datetime.datetime.strptime(enddate, '%Y-%m-%d') - datetime.datetime.strptime(begindate, '%Y-%m-%d')).days)
        list.append(round(diff_precent, 3))
        period_data.append(list)

        if direction == 'left':
            begindate = firstdate
            enddate = date
            endprice = price
        if direction == 'right':
            begindate = date
            enddate = lastdate
            beginprice = price

        diff_days = datetime.datetime.strptime(enddate, '%Y-%m-%d') - datetime.datetime.strptime(begindate, '%Y-%m-%d')
        ismax = not ismax
    return period_data

#result = get_wave(['600570'], start='2017-01-01', duration=0, pchange=0.0)
#print(result)