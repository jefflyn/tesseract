import numpy as np
import pandas as pd

from stocks.app import realtime
from stocks.app import falco
from stocks.app import _utils
from stocks.app import report
from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import wave
from stocks.gene import maup
from stocks.gene import bargain


if __name__ == '__main__':
    data = _datautils.get_industry_data('化学制药.txt')
    codes = list(data['code'])
    limitupdf = limitup.get_limit_up(codes)
    _datautils.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than 3
    limitupcount = limitup.count(limitupdf, 3)
    # print(limitupcount)

    codes = list(limitupcount.index.get_values())
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount[['name','count']], on='name', how='left')
    print(bottomdf)

    # 3.get wave data
    wavedf = wave.get_wave(codes)
    print(wavedf)
    listdf = []
    for code in codes:
        wdf = wavedf[wavedf.code == code]
        listdf.append(wave.format_wave_data(wdf))
    #figure display
    wave.plot_wave(listdf)

    # 4.ma data
    madf = maup.get_ma(codes)
    print(madf)

    # 5.limitup data
    print(limitupdf)



