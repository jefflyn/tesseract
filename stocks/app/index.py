# coding: utf-8
import time
from sys import argv
import pandas as pd
import tushare as ts

from stocks.gene import wave
from stocks.app import _utils
from stocks.data import data_util

pd.set_option('display.width', 600)

INDEX_SH = ['000001', '000016']
INDEX_SZ = ['399001', '399005']
INDEX_CYB = ['399006']

###'000300',
target = ['000001', '000016', '399001', '399005', '399006']

def format_index(df):
    # format data
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['close'] = df['close'].apply(lambda x: str(round(x, 2)))
    df['low'] = df['low'].apply(lambda x: '_' + str(round(x, 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(x, 2)))
    df['bottom'] = df['bottom'].apply(lambda x: '[' + str(x) )
    df['top'] = df['top'].apply(lambda x: str(x) + ']')
    df['uspace'] = df['uspace'].apply(lambda x: '+' + str(round(x, 2)) + '%')
    df['dspace'] = df['dspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    return df


def get_status():
    indexdf = ts.get_index()
    indexdf = indexdf[indexdf['code'].isin(target)]

    result_data = []
    for index, row in indexdf.iterrows():
        row_data = []
        code = row['code']
        row_data.append(code)
        row_data.append(row['name'])
        row_data.append(row['change'])
        current_point = row['close']
        row_data.append(current_point)
        row_data.append(row['low'])
        row_data.append(row['high'])
        row_data.append(row['volume'])
        row_data.append(row['amount'])

        # get wave data and bottom top
        wavedf = wave.get_wave(code, index=True)
        wavestr = wave.wave_to_str(wavedf, size=3)
        bottomdf = wave.get_bottom(wavedf, limit=8)
        bottom = bottomdf.ix[0, 'bottom']
        top = bottomdf.ix[0, 'top']
        positon = (current_point - bottom) / (top - bottom) * 100
        uspace = (current_point - bottom) / bottom * 100
        dspace = (current_point - top) / top * 100

        row_data.append(wavestr)
        row_data.append(bottom)
        row_data.append(round(uspace, 2))
        row_data.append(round(dspace, 2))
        row_data.append(top)
        row_data.append(round(positon, 2))

        suggest = suggest_by_position(code, positon)
        row_data.append(suggest)

        result_data.append(row_data)

    columns = ['code', 'name', 'change', 'close', 'low', 'high', 'volume', 'amount', 'wave', 'bottom', 'uspace',
               'dspace', 'top', 'position', 'suggest']
    resultdf = pd.DataFrame(result_data, columns=columns)

    resultdf = resultdf.sort_values('change', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    print("get index status finish...")
    return resultdf


def suggest_by_position(code, position):
    suggest = ''
    if code in INDEX_SH:
        if _utils.is_inrange(position, 0, 11):
            return 'suck'
        elif _utils.is_inrange(position, 11, 30):
            return 'buy'
        elif   _utils.is_inrange(position, 30, 40):
            return 'hold'
        elif   _utils.is_inrange(position, 40, 55):
            return 'sell'
        elif _utils.is_inrange(position, 55):
            return 'out'
    elif code in INDEX_SZ:
        if _utils.is_inrange(position, 0, 20):
            return 'suck'
        elif _utils.is_inrange(position, 20, 35):
            return 'buy'
        elif   _utils.is_inrange(position, 35, 60):
            return 'hold'
        elif   _utils.is_inrange(position, 60, 75):
            return 'sell'
        elif _utils.is_inrange(position, 75):
            return 'out'
    elif code in INDEX_CYB:
        if _utils.is_inrange(position, 0, 30):
            return 'suck'
        elif _utils.is_inrange(position, 30, 50):
            return 'buy'
        elif   _utils.is_inrange(position, 50, 65):
            return 'hold'
        elif   _utils.is_inrange(position, 65, 75):
            return 'sell'
        elif _utils.is_inrange(position, 75):
            return 'out'
    else:
        return 'shit'


if __name__ == '__main__':
    if len(argv) > 1:
        while True:
            print(format_index(get_status()), end='')
            time.sleep(5)
    else:
        format_index(get_status())
        wavedf = wave.get_wave(codes=target, index=True)
        # plot figure
        listdf = []
        for code in target:
            wdf = wavedf[wavedf.code == code]
            listdf.append(wave.format_wave_data(wdf, index=True))
        # figure display
        wave.plot_wave(listdf, filename='wave_index.png', columns=3)

