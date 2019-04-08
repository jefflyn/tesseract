from datetime import datetime as dtime
import datetime

import numpy as np
import pandas as pd

from stocks.data import data_util
from stocks.app import _utils
import stocks.base.display

histnum = 30
lastmonthstr = (dtime.now() + datetime.timedelta(days=-histnum)).strftime('%Y-%m-%d')


def get_upnday(codes=None, n=0, change=None):
    """
    获取近7天涨跌情况，30天的涨幅
    :param codes:
    :param n:
    :param change:
    :return:
    """
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
        hist_data = data_util.get_hist_trade(code, start=lastmonthstr)
        if hist_data is None or len(hist_data) < 5:
            continue
        latest = hist_data.tail(1)
        idx = latest.index.get_values()[0]
        latest_date_str = latest.at[idx, 'trade_date']
        # excluding halting
        if _utils.is_halting(code, latest_date_str):
            continue

        histndf = hist_data.tail(histnum)
        histndf = histndf.sort_values('trade_date', ascending=False)
        sumup = 0.0
        isndayup = True
        beginp = 0.0
        endp = 0.0
        ndays = 0.0
        volumes = [row[1]['vol'] for row in histndf.iterrows()]
        week_vol = []
        n_vol = 5
        for i in range(n_vol):
            sub_vol = volumes[i + 1:i + 1 + n_vol]
            week_vol.append(volumes[i] / np.mean(sub_vol))
        max_v = np.max(week_vol[:2])
        min_v = np.min(week_vol[2:n_vol])
        multi_vol_rate = round(max_v / min_v, 2)

        change_list = ['0' if c < 0 else '1' for c in histndf[0:7]['pct_change']][::-1]
        change_str = ''.join(change_list)
        sum_30_days = np.sum(histndf['pct_change'])
        for index, row in histndf.iterrows():
            change = float(row['pct_change'])
            close = float(row['close'])

            if endp == 0.0:
                endp = close
            if change < 0:
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

        item = data_util.get_basics(code)
        idx = item.index.get_values()[0]
        nlist = []
        nlist.append(code)
        nlist.append(item.at[idx, 'name'])
        nlist.append(item.at[idx, 'industry'])
        nlist.append(item.at[idx, 'area'])
        nlist.append(change_str)
        nlist.append(round(sum_30_days, 2))
        nlist.append(ndays)
        nlist.append(round(sumup, 2))
        nlist.append(str(np.round(week_vol, 2)))
        nlist.append(multi_vol_rate)
        upndata.append(nlist)

    upndf = pd.DataFrame(upndata,
                         columns=['code', 'name', 'industry', 'area', 'change_7_days', 'sum_30_days', 'updays', 'sumup', 'multi_vol', 'vol_rate'])
    upndf = upndf.sort_values(['updays', 'sumup'], ascending=[False, True])
    return upndf


if __name__ == '__main__':
    # basics = _datautils.get_basics()
    # codes = list(basics['code'])
    codes = ['603106']
    df = get_upnday(codes)
    print(df)
    # _dt.to_db(df, 'up_volume')
