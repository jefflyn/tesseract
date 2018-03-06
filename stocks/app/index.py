# coding: utf-8
from sys import argv
import pandas as pd
import tushare as ts

from stocks.gene import wave

pd.set_option('display.width', 600)

target = ['000001', '000016', '000300', '399001', '399005', '399006']
indexdf = ts.get_index()
indexdf = indexdf[indexdf['code'].isin(target)]
indexdf = indexdf.sort_values('change', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

if __name__ == '__main__':
    print(indexdf[['code','name','change','close','preclose','open','low','high','volume','amount']])
    if len(argv) == 1:
        wavedf = wave.get_wave(codes=target, index=True)
        # plot figure
        listdf = []
        for code in target:
            wdf = wavedf[wavedf.code == code]
            listdf.append(wave.format_wave_data(wdf, index=True))
        # figure display
        wave.plot_wave(listdf, filename='wave_index.png', columns=3)

