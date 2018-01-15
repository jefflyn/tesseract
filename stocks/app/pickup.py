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


def pickup_subnew():
    data = _datautils.get_stock_data(type='c', filename='次新0115.txt')
    codes = list(data['code'])

    # get the bottom price data
    bottomdf = falco.get_monitor(codes)

    # ma data
    madf = maup.get_ma(codes)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma30_space']],
                      on='code', how='left')
    result = result.sort_values('space', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    result['change'] = result['change'].apply(lambda n: str(round(n, 3)) + '%')
    result['space'] = result['space'].apply(lambda n: str(round(n, 3)) + '%')
    result.to_csv('pickup_subnew.csv')

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

def get_limitup_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low) / low * 100

def pickup_s2():
    trade = pd.HDFStore('../data/trade.h5')
    df = trade.select('hist')
    limitupdf = df[(df.p_change > 9.9) & (df['code'].str.get(0) != '3')][['code', 'p_change', 'date', 'low']]
    # limitupdf = df[(df.code == '000002') & (df.p_change > 9.9)][['code','p_change','date','low']]
    _datautils.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=3, condition=[100, 1])
    print('limitupcount size: ' + str(len(limitupcount)))

    codes = list(limitupcount['code'])
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount, on='code', how='left')
    bottomdf['lmtspace'] = bottomdf[['price', 'lmtuplow']].apply(get_limitup_space, axis=1)
    print('bottomdf size: ' + str(len(bottomdf)))

    codes = list(bottomdf['code'])
    # 3.ma data
    madf = maup.get_ma(codes)
    # print(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma30_space']], on='code', how='left')
    # print(result)
    result = result.sort_values(['space', 'lmtuplow'], axis=0, ascending=[True,True], inplace=False, kind='quicksort', na_position='last')
    result['change'] = result['change'].apply(lambda n: str(round(n, 2)) + '%')
    result['space'] = result['space'].apply(lambda n: str(round(n, 2)) + '%')
    result['lmtspace'] = result['lmtspace'].apply(lambda n: str(round(n, 2)) + '%')
    result.to_csv('pickup2.csv')
    _datautils.to_db(result, 'pickup2')

    # wavecodes = list(result['code'])
    # # 4.get wave data
    # wavedf = wave.get_wave(wavecodes[len(wavecodes) - 20 :])
    # # print(wavedf)
    # listdf = []
    # for code in wavecodes:
    #     wdf = wavedf[wavedf.code == code]
    #     listdf.append(wave.format_wave_data(wdf))
    # # figure display
    # wave.plot_wave(listdf, filename='pickup2.png')

if __name__ == '__main__':
    pickup_subnew()
    # bottomdf = falco.get_monitor('002852')
    # print(bottomdf)
    # exit()
    #pickup_s2()
    # pickup_s1('i', '零售.txt')




