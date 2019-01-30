from datetime import datetime as dtime
import datetime

import numpy as np
import pandas as pd

from stocks.data import _datautils
import stocks.base.dbutils as _dt
import stocks.base.display

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
        hist_data = _datautils.get_k_data(code, start=lastmonthstr)
        if hist_data is None or len(hist_data) < 5:
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
        volumes = [row[1]['volume'] for row in histndf.iterrows()]
        week_vol = []
        n_vol = 5
        for i in range(n_vol):
            sub_vol = volumes[i + 1:i + 1 + n_vol]
            week_vol.append(volumes[i] / np.mean(sub_vol))
        max_v = np.max(week_vol[:2])
        min_v = np.min(week_vol[2:n_vol])
        is_multi_vol = round(max_v / min_v, 2)

        for index, row in histndf.iterrows():
            open = float(row['open'])
            close = float(row['close'])

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
        if (isndayup is False and ndays < n) or ndays < n:
            continue
        else:
            if beginp == 0.0:
                continue
            sumup = (endp - beginp) / beginp * 100

        item = _datautils.get_basics(code)
        idx = item.index.get_values()[0]
        nlist = []
        nlist.append(code)
        nlist.append(item.at[idx, 'name'])
        nlist.append(item.at[idx, 'industry'])
        nlist.append(item.at[idx, 'area'])
        nlist.append(ndays)
        nlist.append(round(sumup, 2))
        nlist.append(is_multi_vol)
        nlist.append(str(np.round(week_vol, 2)))
        upndata.append(nlist)

    upndf = pd.DataFrame(upndata,
                         columns=['code', 'name', 'industry', 'area', 'updays', 'sumup', 'multi_vol', 'vol_rate'])
    upndf = upndf.sort_values(['updays', 'sumup'], ascending=[False, True])
    endtime = dtime.now()
    # print("process upnday data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return upndf


if __name__ == '__main__':
    # basics = _datautils.get_basics()
    # codes = list(basics['code'])
    codes = ['300156']
    df = get_upnday(codes)
    print(df)
    # _dt.to_db(df, 'up_volume')
