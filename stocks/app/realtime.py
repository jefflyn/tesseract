import stocks.base.display
from sys import argv
import tushare as ts
from tushare.stock import cons as ct
from stocks.gene import wave
from stocks.data import data_util as _dt
import pandas as pd
import time
from tkinter import *
import stocks.base.sms_util as sms
from stocks.base.redis_util import redis_client
from stocks.base import date_const

keys = ['pa', 'cf', 'df', 'sim']

INDEX_LIST_NEW = dict(zip(list(x[2:] for x in ct.INDEX_LIST.values()), ct.INDEX_LIST.keys()))

pre_key_today = date_const.TODAY + '_'


def format_realtime(df):
    # format data
    df['price'] = df['price'].apply(lambda x: str(round(float(x), 2)))
    df['bid'] = df['bid'].apply(lambda x: str(round(float(x), 2)))
    df['ask'] = df['ask'].apply(lambda x: str(round(float(x), 2)))
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['bottom'] = df['bottom'].apply(lambda x: '[' + str(x))
    df['top'] = df['top'].apply(lambda x: str(x) + ']')
    df['cost'] = df['cost'].apply(lambda x: '<' + str(round(x, 3)) + ', ')
    df['share'] = df['share'].apply(lambda x: str(x) + '>')
    df.insert(15, 'cost, share', df['cost'] + df['share'])
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['amp'] = df['amp'].apply(lambda x: str(round(x, 2)) + '%')
    # df['profit_perc'] = df['profit_perc'].apply(lambda x: str(round(x, 2)) + '%')
    df['uspace'] = df['uspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['dspace'] = df['dspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    df['current'] = df['current'].apply(lambda x: str(round(x, 2)) + '%')

    df = df.drop('cost', 1)
    df = df.drop('share', 1)
    return df


def re_exe(hold_df=None, inc=3, show_wave=True, sortby=None):
    while True:
        real_df = get_realtime(hddf=hold_df, sortby=sortby)
        # filter
        real_df = real_df[real_df.bid > '0.01']
        finaldf = format_realtime(real_df)
        # print(finaldf, end='')
        if show_wave is False:
            del finaldf['wave']
        print(finaldf)
        time.sleep(inc)


def get_realtime(hddf=None, sortby=None):
    codes = list(hddf['code'])
    df = ts.get_realtime_quotes(codes)
    data_list = []
    for index, row in df.iterrows():
        code = row['code']
        code = INDEX_LIST_NEW[code] if code in INDEX_LIST_NEW.keys() else code
        pre_close = float(row['pre_close'])
        price = float(row['price'])
        high = float(row['high'])
        low = float(row['low'])

        price_diff = price - pre_close
        change = price_diff / pre_close * 100

        index = list(hddf['code']).index(code)
        cost = hddf.ix[index, 'cost']
        # cost = cost if cost > 1 else price
        share = hddf.ix[index, 'share']
        wavedf = wave.get_wave(code)
        wavestr = wave.wave_to_str(wavedf, size=3)
        bdf = wave.get_bottom(wavedf)
        bottom = hddf.ix[index, 'bottom']
        bottom_auto = bdf.ix[0, 'bottom']
        bottom_auto_flag = ''
        if bottom is None or bottom_auto < bottom:
            bottom = bottom_auto
            bottom_auto_flag = 'A'

        top = bdf.ix[0, 'top']
        dspace = (price - top) / top * 100
        current = 0
        amplitude = 0
        if high != low:
            current = (price - low) / (high - low) * 100
            amplitude = (high - low) / low * 100
        position = (price - bottom) / (top - bottom) * 100

        cost_diff = price - cost
        profit = cost_diff * share if share > 0 else 0

        if profit < 0 and price > 0:
            profit_perc = (cost / price - 1) * -100.0
        else:
            profit_perc = cost_diff / cost * 100.0 if profit > 0 else 0

        # calculate the bottom, the smaller the possibility of bounce is bigger.
        # if negative, that means the bottom is broken, pay much attention if get out or wait for the escape line
        btm_diff = price - bottom
        # esc_diff = (price - escape) if (btm_diff < 0) else (bottom - escape)

        btm_space = btm_diff / bottom * 100.0
        # esc_space = esc_diff / escape * 100.0

        warn_sign = ''
        if profit > 0:
            warn_sign = '$'
        elif btm_diff <= 0 or low < bottom or bottom_auto_flag == 'A':
            warn_sign = '!'

        # 告警短信:价格、涨跌幅、止损、止盈等
        if low < bottom or btm_space < 5 or change > 7 or change < -6:
            name_format = '：' + code + ' ' + row['name']
            change_str = str(round(change, 2)) + '%' if change < 0 else '+' + str(round(change, 2)) + '%'
            price_format = str(round(price, 2)) + change_str
            if len(price_format) < 12:
                price_format = str(round(price, 2)) + ' ' + change_str
            warn_times = redis_client.get(pre_key_today + code)
            if warn_times is None:
                try:
                    redis_client.set(pre_key_today + code, row['name'] + price_format)
                    sms.send_msg(code, name_format, price_format)
                except Exception as e:
                    print(e)


        curt_data = []
        curt_data.append(warn_sign)
        curt_data.append(change)
        curt_data.append(amplitude)
        curt_data.append(cost)
        curt_data.append(profit)
        curt_data.append(profit_perc)
        profit_str = str(round(profit, 2)) + ', ' + str(round(profit_perc, 2)) + '%'
        curt_data.append(profit_str)
        curt_data.append(wavestr)
        curt_data.append(str(bottom) + bottom_auto_flag)
        curt_data.append(btm_space)
        curt_data.append(dspace)
        curt_data.append(top)
        curt_data.append(current)
        curt_data.append(position)
        curt_data.append(share)
        curt_data.append(price * share)
        data_list.append(curt_data)

    df_append = pd.DataFrame(data_list,
                             columns=['Y', 'change', 'amp', 'cost', 'profit_amt', 'profit_perc', 'profit', 'wave', 'bottom',
                                      'uspace', 'dspace', 'top', 'current', 'position', 'share', 'capital'])
    df = df.join(df_append)

    df = df[df.price > '1']
    # df['change'] = df['change'].astype('float32')
    # df['profit_perc'] = df['profit_perc'].astype('float32')
    if sortby == 'p':
        df = df.sort_values(['profit_perc'], axis=0, ascending=True, inplace=False, kind='quicksort',
                            na_position='last')
    elif sortby == 'b':
        df = df.sort_values(['uspace'], axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    elif sortby == 't':
        df = df.sort_values(['capital'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    else:
        df = df.sort_values(['change'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    return df[
        ['Y', 'code', 'name', 'price', 'change', 'amp', 'bid', 'ask', 'low', 'high', 'current', 'wave', 'bottom', 'uspace', 'dspace',
         'top', 'position', 'cost', 'share', 'capital', 'profit']]


if __name__ == '__main__':
    """
    python realtime.py df 1 false p

    """
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python realtime.py df ...")
        sys.exit(0)
    type = argv[1]
    if type not in keys:
        print("File name NOT found. Try the followings: " + str(keys))
        sys.exit(0)
    # hold = argv[2] if len(argv) > 2 else 1
    # display = True if (len(argv) > 3 and str(argv[3]).upper() == 'TRUE') else False
    # sort = argv[4] if len(argv) > 4 else None
    hold_df = _dt.get_my_stock_pool(type)
    if hold_df.empty:
        print("Stock NOT hold! Auto change to default mode.")
        hold_df = _dt.get_my_stock_pool(type, 0)
    re_exe(hold_df, 3)

