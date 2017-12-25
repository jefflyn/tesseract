from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as dt

pd.set_option('display.width', 600)

lastmonthstr = (datetime.datetime.now() - 30).strftime('%Y-%m-%d')

def upnday(codes=None, n=3, change=None):
    starttime = datetime.datetime.now()
    print("process upnday data start at [%s]" % starttime)
    print("get k data from %s" % lastmonthstr)
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
        latest_date = datetime.datetime.strptime(latest_date_str, '%Y-%m-%d')
        delta = starttime - latest_date
        # excluding halting
        if (delta.days > 3):
            print(code + ' halting...')
            continue

        histndf = hist_data.tail(n)
        for index, row in histndf.iterrows():
            open = float(row['open'])
            close = float(row['close'])



        row = dt.get_basics(code)
        idx = row.index.get_values()[0]
        malist = []
        malist.append(code)
        malist.append(row.at[idx, 'name'])
        malist.append(row.at[idx, 'industry'])
        malist.append(row.at[idx, 'area'])
        malist.append(row.at[idx, 'pe'])
        malist.append(round(ma5,2))
        malist.append(round(ma10,2))
        malist.append(round(ma20,2))
        malist.append(round(ma30,2))
        malist.append(round(ma60,2))
        malist.append(round(ma90,2))
        malist.append(round(ma120,2))
        malist.append(round(ma250,2))
        malist.append(ma30std)
        malist.append(ma60std)
        malist.append(ma120std)
        malist.append(ma250std)

        upndata.append(malist)

    upndf = pd.DataFrame(upndata, columns=['code', 'name', 'industry', 'area', 'pe', \
                                      'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250', \
                                            'ma30std','ma60std','ma120std','ma250std'])
    endtime = datetime.datetime.now()
    print("process upnday data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return upndf




if __name__ == '__main__':
    df = get_ma('002620', start='2017-01-01')
    df = get_ma_up(df)
    print(df)