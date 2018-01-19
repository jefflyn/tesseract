# coding: utf-8
import pandas as pd
import tushare as ts

from stocks.gene import wave

pd.set_option('display.width', 600)

myindex = ['000001','000016','000300','399001','399005','399006']
indexdf = ts.get_index()
indexdf = indexdf[indexdf['code'].isin(myindex)]
indexdf = indexdf.sort_values('change', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
print(indexdf)

wavedf = wave.get_wave(myindex)
formatdata = wave.format_wave_data(wavedf)
wave.plot_wave(formatdata, filename='wave_index.png')

