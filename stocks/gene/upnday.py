from datetime import datetime as dtime
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as dt

pd.set_option('display.width', 600)

histnum = 30
lastmonthstr = (dtime.now() + datetime.timedelta(days=-histnum)).strftime('%Y-%m-%d')


def get_upnday(codes=None, n=0, change=None):
    starttime = dtime.now()
    # print("process upnday data start at [%s]" % starttime)
    # print("get k data from %s" % lastmonthstr)
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    upndata = []
    for code in code_list:
        hist_data = dt.get_k_data(code, start=lastmonthstr)
        if hist_data is None or len(hist_data) == 0:
            continue
        latest = hist_data.tail(1)
        idx = latest.index.get_values()[0]
        latest_date_str = latest.at[idx, 'date']
        latest_date = dtime.strptime(latest_date_str, '%Y-%m-%d')
        delta = starttime - latest_date
        # excluding halting
        if (delta.days > 3):
            print(code + ' halting...')
            continue

        histndf = hist_data.tail(histnum)
        histndf = histndf.sort_values('date', ascending=False)
        sumup = 0.0
        isndayup = True
        beginp = 0.0
        endp = 0.0
        ndays = 0.0
        is_multi_vol = False
        day1vol = 0
        day2vol = 0
        for index, row in histndf.iterrows():
            open = float(row['open'])
            close = float(row['close'])
            volume = float(row['volume'])
            if index == 0:
                day1vol = volume
            if index == 1:
                day2vol = volume
            if endp == 0.0:
                endp = close
            diff = close - open
            if diff < 0:
                if index == 0:
                    continue
                isndayup = False
                beginp = close
                break
            else:
                ndays += 1
        # not matche the n-days-up rule
        if (isndayup == False and ndays < n) or ndays < n:
            continue
        else:
            if beginp == 0.0:
                continue
            sumup = (endp - beginp) / beginp * 100

        item = dt.get_basics(code)
        idx = item.index.get_values()[0]
        nlist = []
        nlist.append(code)
        nlist.append(item.at[idx, 'name'])
        nlist.append(item.at[idx, 'industry'])
        nlist.append(item.at[idx, 'area'])
        nlist.append(item.at[idx, 'pe'])
        nlist.append(ndays)
        nlist.append(round(sumup,2))
        if day2vol * 2.1 < day1vol:
            is_multi_vol = True
        nlist.append(is_multi_vol)

        upndata.append(nlist)

    upndf = pd.DataFrame(upndata, columns=['code', 'name', 'industry', 'area', 'pe', 'updays', 'sumup', 'multi_vol'])
    upndf = upndf.sort_values(['updays', 'sumup'], ascending=[False, True])
    endtime = dtime.now()
    # print("process upnday data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return upndf


if __name__ == '__main__':
    df = get_upnday('002902')
    print(df)