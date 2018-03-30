# coding: utf-8
import time
from sys import argv
import pandas as pd
import tushare as ts

from stocks.gene import wave
from stocks.app import _utils
from stocks.data import _datautils

pd.set_option('display.width', 600)

INDEX_SH = ['000001', '000016', '000300']
INDEX_SZ = ['399001', '399005']
INDEX_CYB = ['399006']

target = ['000001', '000016', '000300', '399001', '399005', '399006']


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
        bottomdf = wave.get_bottom(wavedf, limit=8)
        bottom = bottomdf.ix[0, 'bottom']
        top = bottomdf.ix[0, 'top']
        positon = (current_point - bottom) / (top - bottom) * 100
        space = (current_point - bottom) / bottom * 100

        row_data.append(bottom)
        row_data.append(round(space, 2))
        row_data.append(top)
        row_data.append(round(positon, 2))

        suggest = suggest_by_position(code, positon)
        row_data.append(suggest)

        result_data.append(row_data)

    columns = ['code', 'name', 'change', 'close', 'low', 'high', 'volume', 'amount','bottom', 'space', 'top', 'position', 'suggest']
    resultdf = pd.DataFrame(result_data, columns=columns)

    resultdf = resultdf.sort_values('position', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')

    _datautils.to_db(resultdf, 'index_status')
    resultdf.to_csv('index_status.csv')
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
            print(get_status())
            time.sleep(60)
    else:
        wavedf = wave.get_wave(codes=target, index=True)
        # plot figure
        listdf = []
        for code in target:
            wdf = wavedf[wavedf.code == code]
            listdf.append(wave.format_wave_data(wdf, index=True))
        # figure display
        wave.plot_wave(listdf, filename='wave_index.png', columns=3)

