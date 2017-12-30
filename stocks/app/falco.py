import time

import pandas as pd

import tushare as ts

from stocks.data import _datautils
from stocks.gene import period
from stocks.gene import bargain


def get_monitor(codes, limit=10):
    basics = _datautils.get_basics()
    df = ts.get_realtime_quotes(codes)
    data_list = []
    for index, row in df.iterrows():
        code = row['code']
        info = basics[basics['code'].astype(object) == code]
        idx = info.index.tolist()[0]
        industry = info.at[idx, 'industry']
        area = info.at[idx, 'area']
        pe = info.at[idx, 'pe']

        # print(code)
        pre_close = float(row['pre_close'])
        price = float(row['price'])
        low = float(row['low'])

        price_diff = price - pre_close
        change = price_diff / pre_close * 100

        codelist = list(_datautils.get_bottom()['code'])
        bottom = 0
        if code in codelist:
            index = codelist.index(code)
            bottom = _datautils.get_bottom().ix[index, 'bottom']
        else:
            wavedf = period.get_wave(code)
            bottomdf = bargain.get_bottom(wavedf, limit=limit)
            bottom = bottomdf.at[bottomdf.index.get_values()[0], 'bottom']
        ##calculate the bottom, the smaller the possibility of bounce is bigger.
        ##if negative, that means the bottom is broken, pay much attention if get out or wait for the escape line
        btm_diff = price - bottom
        btm_space = btm_diff / bottom * 100.0

        warn_sign = ''
        if btm_diff <= 0 or low < bottom:
            warn_sign = '!!!'

        curt_data = []
        curt_data.append(warn_sign)
        curt_data.append(change)
        curt_data.append(bottom)
        curt_data.append(btm_space)
        curt_data.append(industry)
        curt_data.append(area)
        curt_data.append(pe)
        data_list.append(curt_data)

    df_append = pd.DataFrame(data_list, columns=['warn', 'change', 'bottom', 'space', 'industry', 'area', 'pe'])
    df = df.join(df_append)
    df = df.sort_values('space', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    df['change'] = df['change'].apply(lambda n: str(round(n, 3)) + '%')
    df['space'] = df['space'].apply(lambda n: str(round(n, 3)) + '%')
    return df

def monitor(codes, inc=3):
    while True:
        df = get_monitor(codes)
        print(df[['warn','code','name','change','price','low','bottom','space','industry','area','pe']])

        time.sleep(inc)

