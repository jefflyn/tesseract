from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

def get_wave(codes=None, start=None, end=None, beginlow=True):
    starttime = datetime.datetime.now()
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else: code_list = codes

    period_data = []
    for code in code_list:
        hist_data = ts.get_k_data(code, start)
        if hist_data is None or len(hist_data) == 0:
            continue

        min_price = hist_data.min()['low']
        min_rec = hist_data[hist_data.low == min_price]
        print(min_rec)
        idx_min = min_rec.index.get_values()[0]
        min_date = min_rec.at[idx_min,'date']
        min_close = min_rec.at[idx_min,'close']

        ismax = beginlow
        begindate = datetime.datetime.strptime(start, '%Y-%m-%d')
        enddate = min_date
        beginprice = min_price
        endprice = min_price
        list = []
        while (datetime.datetime.strptime(enddate, '%Y-%m-%d') - begindate).days >= 30:
            pre_data = hist_data[(hist_data.date >= start) & (hist_data.date < enddate)]

            print(ismax)
            beginprice = pre_data.max()['high'] if ismax else pre_data.min()['low']

            pre_rec = pre_data[pre_data.high == beginprice] if ismax else pre_data[pre_data.low == beginprice]

            pre_idx = pre_rec.index.get_values()[0]
            pre_date = pre_rec.at[pre_idx, 'date']
            enddate = pre_date
            ismax = False
            # ['code', 'begin', 'end', 'status' 'begin_price', 'end_price', 'days', 'p_change']
            list.append(code)
            list.append(pre_date)
            list.append(code)
            list.append(code)
            list.append(code)
            list.append(code)
            list.append(code)
            list.append(code)


        print(list)

        max_data = hist_data[(hist_data.date > min_date)]
        max_price = max_data.max()['high']
        max_rec = max_data[max_data.high == max_price]
        print(max_rec)
        idx_max = max_rec.index.get_values()[0]
        max_date = max_rec.at[idx_max, 'date']
        max_close = max_rec.at[idx_max, 'close']

        min_datetime = datetime.datetime.strptime(min_date, '%Y-%m-%d')
        max_datetime = datetime.datetime.strptime(max_date, '%Y-%m-%d')
        delta = max_datetime - min_datetime
        print(delta)
        print((max_price - min_close) / min_close * 100)

        # latest = hist_data.tail(1)
        # idx = latest.index.get_values()[0]
        # latest_date_str = latest.at[idx, 'date']
        # latest_date = datetime.datetime.strptime(latest_date_str, '%Y-%m-%d')
        # delta = starttime - latest_date

    period_df = pd.DataFrame(period_data, \
                             columns=['code', 'begin', 'end', 'status' 'begin_price', 'end_price', 'days', 'p_change'])

    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
    return period_df

get_wave('600570', start='2016-10-01')