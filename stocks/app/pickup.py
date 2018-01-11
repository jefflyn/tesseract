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

def pickup_s1(type='', classname=''):
    data = _datautils.get_stock_data(type=type, filename=classname)
    codes = list(data['code'])
    limitupdf = limitup.get_limit_up(codes)
    _datautils.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=3, condition=[90,1])
    # print(limitupcount)

    codes = list(limitupcount.index.get_values())
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount[['name', 'count']], on='name', how='left')
    # print(bottomdf)

    # 3.ma data
    madf = maup.get_ma(codes)
    # print(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma30_space']],
                      on='code', how='left')
    result.to_csv('pickup.csv')
    exit()

    #########
    wavecodes = list(result['code'])
    # 4.get wave data
    wavedf = wave.get_wave(wavecodes)
    # print(wavedf)
    listdf = []
    for code in wavecodes:
        wdf = wavedf[wavedf.code == code]
        listdf.append(wave.format_wave_data(wdf))
    # figure display
    wave.plot_wave(listdf, filename='pickup.png')

    # 5.limitup data
    print(limitupdf)


def pickup_s2():
    tradecomp = pd.HDFStore('../data/trade_comp.h5')
    df = tradecomp.select('hist')
    df = df[(df.p_change > 9.9) & (df['code'].str.get(0) != '3')][['code']]
    df = df.drop_duplicates(['code'])
    codes = list(df['code'])

    limitupdf = limitup.get_limit_up(codes)
    _datautils.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=3, condition=[100, 1])
    # print(limitupcount)

    codes = list(limitupcount.index.get_values())
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)

    # 3.ma data
    madf = maup.get_ma(codes)
    # print(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma30_space']],
                      on='code', how='left')
    # print(result)
    result.to_csv('pickup2.csv')
    exit()

if __name__ == '__main__':
    # bottomdf = falco.get_monitor('002852')
    # print(bottomdf)
    # exit()
    pickup_s2()
    # pickup_s1('i', '零售.txt')




