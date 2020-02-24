import sys
import time
from sys import argv

import pandas as pd
import tushare as ts
from tushare.stock import cons as ct

from stocks.data import data_util as _dt
from stocks.gene import wave
from stocks.util import date_util

keys = ['pa', 'cf', 'df', 'sim', 'gap']

INDEX_LIST_NEW = dict(zip(list(x[2:] for x in ct.INDEX_LIST.values()), ct.INDEX_LIST.keys()))

pre_key_today = date_util.get_today() + '_'


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
    # df['amp'] = df['amp'].apply(lambda x: str(round(x, 2)) + '%')
    # df['profit_perc'] = df['profit_perc'].apply(lambda x: str(round(x, 2)) + '%')
    df['uspace'] = df['uspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['dspace'] = df['dspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    df['current'] = df['current'].apply(lambda x: str(round(x, 2)) + '%')
    df['o_gap'] = df['o_gap'].apply(lambda x: '[' + str(round(x, 2)) + '%, ')
    df['g_scale'] = df['g_scale'].apply(lambda x: str(round(x, 2)) + '%] ')
    # df['g_space'] = df['g_space'].apply(lambda x: str(round(x, 2)) + '%]')
    df = df.drop('g_space', 1)
    df = df.drop('cost', 1)
    df = df.drop('share', 1)
    return df


def re_exe(hold_df=None, inc=2, show_wave=True, sortby=None):
    if hold_df is None or hold_df.empty:
        print('no stock found!!!')
        return
    codes = list(hold_df['code'])
    last_trade_data = _dt.get_last_trade_data(codes)
    while True:
        real_df = get_realtime(hddf=hold_df, last_trade_data=last_trade_data, sortby=sortby)
        # filter
        # real_df = real_df[real_df.bid > '0.01']
        finaldf = format_realtime(real_df)
        # print(finaldf, end='')
        if show_wave is False:
            del finaldf['wave']
        print(finaldf)
        time.sleep(inc)


def get_realtime(hddf=None, last_trade_data=None, sortby=None):
    codes = list(hddf['code'])
    df = ts.get_realtime_quotes(codes)
    data_list = []
    for index, row in df.iterrows():
        code = row['code']
        code = INDEX_LIST_NEW[code] if code in INDEX_LIST_NEW.keys() else code
        # print(code)
        pre_close = float(row['pre_close'])
        price = float(row['price'])
        open = float(row['open'])
        high = float(row['high'])
        low = float(row['low'])
        last_high = last_trade_data.at[code, 'high']
        last_low = last_trade_data.at[code, 'low']
        open_gap = 0
        gap_scale = 0
        gap_space = 0
        if gap_scale == 0:
            # 向上跳空
            if open > last_high:
                open_gap = round((open - last_high) / last_high * 100, 2)
                if low - last_high > 0:
                    gap_scale = round((low - last_high) / last_high * 100, 2)
                    # 计算缺口和现价的空间
                    gap_space = round((price - last_high) / last_high * 100, 2)
            # 向下跳空缺口
            elif open < last_low:
                open_gap = round((open - last_low) / last_low * 100, 2)
                if high - last_low < 0:
                    gap_scale = round((high - last_low) / last_low * 100, 2)
                    # 计算缺口和现价的空间
                    gap_space = round((price - last_low) / last_low * 100, 2)
        price_diff = price - pre_close
        change = price_diff / pre_close * 100

        index = list(hddf['code']).index(code)
        cost = hddf.loc[index, 'cost']
        cost = cost if cost is not None and str(cost) != 'nan' else price
        share = hddf.loc[index, 'share']
        wavedf = wave.get_wave(code)
        wavestr = wave.wave_to_str(wavedf, 6)
        wave_ab = wave.get_wave_ab_fast(wavestr, 33)
        wave_a = wave_ab[0][0]
        wave_b = wave_ab[1][0]

        bdf = wave.get_bottom(wavedf)
        bottom = hddf.loc[index, 'bottom']
        bottom_auto = bdf.loc[bdf.index[0], 'bottom']
        bottom_auto_flag = ''
        if bottom is None or str(bottom) == 'nan' or bottom_auto < bottom:
            bottom = bottom_auto
            bottom_auto_flag = 'A'

        top = bdf.at[0, 'top']
        dspace = (price - top) / top * 100
        current = 0
        amplitude = 0
        if high != low:
            current = (price - low) / (high - low) * 100
            amplitude = (high - low) / low * 100
        elif high == low:
            current = 100
        position = (price - bottom) / (top - bottom) * 100

        cost_diff = price - cost
        profit = cost_diff * share if share > 0 else 0

        if profit < 0 < price:
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

        curt_data = [warn_sign, open_gap, gap_scale, gap_space, change, amplitude, cost, profit, profit_perc]
        profit_str = str(round(profit, 2)) + ', ' + str(round(profit_perc, 2)) + '%'
        curt_data.append(profit_str)
        curt_data.append(str(wave_a) + '|' + str(round(wave_b, 2)))
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
                             columns=['Y', 'o_gap', 'g_scale', 'g_space', 'change', 'amp', 'cost',
                                      'profit_amt', 'profit_perc', 'profit', 'wave', 'bottom',
                                      'uspace', 'dspace', 'top', 'current', 'position',
                                      'share', 'capital'])
    df = df.join(df_append)

    df = df[df.price > '1']
    if sortby == 'p':
        df = df.sort_values(['profit_perc'], axis=0, ascending=True, inplace=False, kind='quicksort',
                            na_position='last')
    elif sortby == 'b':
        df = df.sort_values(['uspace'], axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    elif sortby == 'g':
        df = df.sort_values(['o_gap', 'g_scale', 'g_space'], axis=0, ascending=True, inplace=False, kind='quicksort',
                            na_position='last')
    else:
        df = df.sort_values(['change'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    return df[
        ['Y', 'code', 'name', 'price', 'o_gap', 'g_scale', 'g_space', 'change', 'bid', 'ask', 'low', 'high',
         'current', 'wave', 'bottom', 'uspace', 'dspace', 'top', 'position', 'cost', 'share', 'capital', 'profit']]


if __name__ == '__main__':
    """
    python realtime.py df 1 false p
    nohup /usr/local/bin/redis-server /usr/local/etc/redis.conf &
    nohup /usr/local/bin/redis-server /etc/redis.conf &
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
    sort = argv[2] if len(argv) > 2 else None
    hold_df = _dt.get_my_stock_pool(type)
    if hold_df.empty:
        print("Stock NOT hold! Auto change to default mode.")
        hold_df = _dt.get_my_stock_pool(type, 0)
    re_exe(hold_df, 3, sortby=sort)
