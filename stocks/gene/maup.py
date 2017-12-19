from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as dt

pd.set_option('display.width', 600)

def get_ma(codes=None, start='2016-01-04', end=None):
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
        latest_date_str = latest.at[idx, 'date']
        latest_date = datetime.datetime.strptime(latest_date_str, '%Y-%m-%d')
        delta = starttime - latest_date
        # 可能停牌，排除
        if (delta.days > 3):
            print(code + "停牌")
            continue

        ma5 = hist_data.tail(5).mean()['close']
        ma10 = hist_data.tail(10).mean()['close']
        ma20 = hist_data.tail(20).mean()['close']
        ma30 = hist_data.tail(30).mean()['close']
        ma60 = hist_data.tail(60).mean()['close']
        ma90 = hist_data.tail(90).mean()['close']
        ma120 = hist_data.tail(120).mean()['close']
        ma250 = hist_data.tail(250).mean()['close']

        row = dt.get_basics(code)
        idx = row.index.get_values()[0]
        malist = []
        malist.append(code)
        malist.append(row.at[idx, 'name'])
        malist.append(row.at[idx, 'industry'])
        malist.append(row.at[idx, 'area'])
        malist.append(row.at[idx, 'pe'])
        malist.append(ma5)
        malist.append(ma10)
        malist.append(ma20)
        malist.append(ma30)
        malist.append(ma60)
        malist.append(ma90)
        malist.append(ma120)
        malist.append(ma250)

        madfdata.append(malist)

    ma_df = pd.DataFrame(madfdata, columns=['code', 'name', 'industry', 'area', 'pe', \
                                      'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250'])
    endtime = datetime.datetime.now()
    print("process ma data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return ma_df


# all 1 year takes about 330s
def get_limit_up(codes = None, start = None, end = None, up = True):
    print("get limitups... ")
    starttime = datetime.datetime.now()
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
        hist_data = hist_data[['code', 'date', 'p_change']]
        hist_data = hist_data[hist_data['p_change'] >= 9.9] if up else hist_data[hist_data['p_change'] <= -9.9]
        # hist_data.reset_index()
        result = result.append(hist_data, ignore_index=True)
    endtime = datetime.datetime.now()
    print("total time: %ds" % (endtime - starttime).seconds)
    return result

def count(df=None):
    if df.empty:
        return df

    df = df[df['p_change'] >= 9.9]
    # dfgroup = df.groupby("code")['p_change'].count()
    dfgroup = df.groupby("code").agg({'p_change': np.size})
    dfgroup = dfgroup.sort_values('p_change', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return dfgroup

if __name__ == '__main__':
    df = get_ma('002620', start='2017-01-01')
    print(df)