from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as dt
from stocks.app import _utils

pd.set_option('display.width', 600)

def get_ma(codes=None, start='2017-01-04', end=None):
    starttime = datetime.datetime.now()
    print("process ma data start at [%s]" % starttime)
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    madfdata = []
    for code in code_list:
        hist_data = dt.get_k_data(code, start=start)
        if hist_data is None or len(hist_data) == 0:
            continue
        latest = hist_data.tail(1)
        idx = latest.index.get_values()[0]
        price = latest.at[idx, 'close']
        latest_date_str = latest.at[idx, 'date']
        # excluding halting
        if (_utils.is_halting(code, latest_date_str)):
            continue

        ma5 = hist_data.tail(5).mean()['close']
        ma10 = hist_data.tail(10).mean()['close']
        ma20 = hist_data.tail(20).mean()['close']
        ma30 = hist_data.tail(30).mean()['close']
        ma60 = hist_data.tail(60).mean()['close']
        ma90 = hist_data.tail(90).mean()['close']
        ma120 = hist_data.tail(120).mean()['close']
        ma250 = hist_data.tail(250).mean()['close']

        ma30ls = [ma5, ma10, ma20, ma30]
        ma60ls = [ma5,ma10,ma20,ma30,ma60]
        ma120ls = [ma5,ma10,ma20,ma30,ma60,ma90,ma120]
        ma250ls = [ma5,ma10,ma20,ma30,ma60,ma90,ma120,ma250]

        ma30std = np.std(np.array(ma30ls))
        ma60std = np.std(np.array(ma60ls))
        ma120std = np.std(np.array(ma120ls))
        ma250std = np.std(np.array(ma250ls))

        isup = (ma10 >= ma20) & (ma20 >= ma30)

        row = dt.get_basics(code)
        idx = row.index.get_values()[0]
        malist = []
        malist.append(code)
        malist.append(row.at[idx, 'name'])
        malist.append(row.at[idx, 'industry'])
        malist.append(row.at[idx, 'area'])
        malist.append(row.at[idx, 'pe'])
        malist.append(isup)
        malist.append(price)
        malist.append(round(ma5,2))
        malist.append(round(ma10,2))
        malist.append(round(ma20,2))
        malist.append(round(ma30,2))
        malist.append(round(ma60,2))
        malist.append(round(ma90,2))
        malist.append(round(ma120,2))
        malist.append(round(ma250,2))
        malist.append(round(ma30std,3))
        malist.append(round((price - ma10) / ma10 * 100, 3))
        # malist.append(ma60std)
        # malist.append(ma120std)
        # malist.append(ma250std)

        madfdata.append(malist)

    ma_df = pd.DataFrame(madfdata, columns=['code', 'name', 'industry', 'area', 'pe', 'isup', 'price', \
                                      'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250', 'ma30std', 'ma10_space'])#,'ma60std','ma120std','ma250std'])
    ma_df = ma_df.sort_values(by=['isup', 'ma10_space'], ascending=[False, True])
    endtime = datetime.datetime.now()
    print("process ma data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return ma_df


# filter ma data
def get_ma_up(madf = None):
    if madf is None:
        return madf
    result = madf[(madf.ma5 >= madf.ma10) & (madf.ma10 >= madf.ma20) & (madf.ma20 >= madf.ma30)]
    return result



if __name__ == '__main__':
    basics = dt.get_basics(excludeCyb=True)
    codes = basics['code'].values
    codes = ['002620']

    df = get_ma(codes, start='2017-01-01')
    # data = maup.get_ma_up(df)

    # data.to_csv("../data/tmp/maupx.csv", encoding='utf-8')
    print(df)