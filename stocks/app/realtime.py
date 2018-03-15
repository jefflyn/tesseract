import sys
from sys import argv
import tushare as ts
from tushare.stock import cons as ct
import pandas as pd
import time
from tkinter import *

pd.set_option('display.width',800)

include_files = {
    'pa': '../data/app/pa.txt',
    'cf': '../data/app/cf.txt',
    'ot': '../data/app/other.txt'
}
keys = list(include_files.keys())

INDEX_LIST_NEW = dict(zip(list(x[2:] for x in ct.INDEX_LIST.values()), ct.INDEX_LIST.keys()))


def format_realtime(df):
    # format data
    df['price'] = df['price'].apply(lambda x: str(round(float(x), 2)))
    df['bid'] = df['bid'].apply(lambda x: str(round(float(x), 2)))
    df['ask'] = df['ask'].apply(lambda x: str(round(float(x), 2)))
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['bottom'] = df['bottom'].apply(lambda x: '[' + str(x) + ']')
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['profit_perc'] = df['profit_perc'].apply(lambda x: str(round(x, 2)) + '%')
    df['btm_space'] = df['btm_space'].apply(lambda x: str(round(x, 2)) + '%')
    return df

def re_exe(file=None, inc=3, sortby=None):
    while True:
        try:
            df = get_realtime(file=file, sortby=sortby)
            # filter
            df = df[df.bid > '0.01']
            df = format_realtime(df)
            print(df)
        except Exception as e:
            print('excpetion: ' + e)
        time.sleep(inc)

def get_realtime(file, sortby=None):
    filePath = include_files[file]
    hddf = pd.read_csv(filePath, sep=' ')
    hddf['code'] = hddf['code'].astype('str').str.zfill(6)
    codes = list(hddf['code'])
    df = ts.get_realtime_quotes(codes)
    data_list = []
    for index, row in df.iterrows():
        code = row['code']

        code = INDEX_LIST_NEW[code] if code in INDEX_LIST_NEW.keys() else code

        pre_close = float(row['pre_close'])
        price = float(row['price'])
        low = float(row['low'])

        price_diff = price - pre_close
        change = price_diff / pre_close * 100

        index = list(hddf['code']).index(code)
        cost = hddf.ix[index, 'cost']
        share = hddf.ix[index, 'share']
        bottom = hddf.ix[index, 'bottom']

        cost_diff = price - cost
        profit = (cost_diff) * share

        if profit < 0 and price > 0:
            profit_perc = (cost / price - 1) * -100.0
        else:
            profit_perc = cost_diff / cost * 100.0

        ##calculate the bottom, the smaller the possibility of bounce is bigger.
        ##if negative, that means the bottom is broken, pay much attention if get out or wait for the escape line
        btm_diff = price - bottom
        # esc_diff = (price - escape) if (btm_diff < 0) else (bottom - escape)

        btm_space = btm_diff / bottom * 100.0
        # esc_space = esc_diff / escape * 100.0

        warn_sign = ''
        if profit > 0:
            warn_sign = '$$$'
        elif btm_diff <= 0 or low < bottom:
            warn_sign = '!!!'

        curt_data = []
        curt_data.append(warn_sign)
        curt_data.append(change)
        curt_data.append(str(cost))
        curt_data.append(profit)
        curt_data.append(profit_perc)
        curt_data.append(str(bottom))
        # curt_data.append(esc_diff)
        curt_data.append(btm_space)
        curt_data.append(share)
        curt_data.append(price * share)
        data_list.append(curt_data)

    df_append = pd.DataFrame(data_list, columns=['warn', 'change', 'cost', 'profit_amt', 'profit_perc', 'bottom', 'btm_space', 'share', 'total_amt'])
    df = df.join(df_append)

    df = df[df.price > '1']
    # df['change'] = df['change'].astype('float32')
    # df['profit_perc'] = df['profit_perc'].astype('float32')
    if sortby == 'p':
        df = df.sort_values(['profit_perc'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    elif sortby == 'b':
        df = df.sort_values(['btm_space'], axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    else:
        df = df.sort_values(['share','change'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    return df[['warn', 'code', 'name', 'price', 'change', 'bid', 'ask', 'low', 'high', 'bottom', 'btm_space', 'cost', 'profit_amt', 'profit_perc', 'share', 'total_amt']]

if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py arg1 ...")
        sys.exit(0)
    file = argv[1]
    sort = argv[2] if len(argv) > 2 else None
    re_exe(file, 3, sort)
    if file not in keys:
        print("File name NOT found. Try the followings: " + str(keys))
        sys.exit(0)










