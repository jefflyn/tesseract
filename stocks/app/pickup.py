import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import tushare as ts

from stocks.app import realtime
from stocks.app import falco
from stocks.app import _utils
from stocks.app import report
from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import wave
from stocks.gene import maup
from stocks.gene import bargain

def pickup_subnew_issue_space():
    subnewbasic = _datautils.get_subnew()
    codes = list(subnewbasic['code'])
    # codes = ['601108']
    # get the bottom price data
    df = ts.get_realtime_quotes(codes)
    subnewbasic = subnewbasic.set_index('code')

    data_list = []
    for index, row in df.iterrows():
        code = row['code']
        current_price = float(row['price'])
        timeToMarket = subnewbasic.ix[code, 'timeToMarket']
        if timeToMarket == 0 or current_price <= 0:
            continue;
        timeToMarket = str(timeToMarket)
        timeToMarket = timeToMarket[0:4] + '-' + timeToMarket[4:6] + '-' + timeToMarket[6:8]
        firstData = _datautils.get_k_data(code, start=timeToMarket, end=timeToMarket)
        issue_close_price = float(firstData.ix[0, 'close'])
        issue_space = (current_price - issue_close_price) / issue_close_price * 100

        curt_data = []
        curt_data.append(issue_close_price)
        curt_data.append(issue_space)
        data_list.append(curt_data)
    df_append = pd.DataFrame(data_list, columns=['issue_close_price', 'issue_space'])
    df = df.join(df_append)

    df = df.sort_values('issue_space', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    df['issue_space'] = df['issue_space'].apply(lambda x: str(round(x, 3)) + '%')
    df = df[['code', 'name', 'price', 'issue_close_price', 'issue_space']]

    df.to_csv('pickup_subnew_issue_space.csv')
    _datautils.to_db(df, 'pickup_subnew_issue_space')


def pickup_subnew():
    data = _datautils.get_subnew()
    codes = list(data['code'])

    # get the bottom price data
    bottomdf = falco.get_monitor(codes)

    # ma data
    madf = maup.get_ma(codes)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma10_space']],
                      on='code', how='left')
    result = result.sort_values('space', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    result['change'] = result['change'].apply(lambda n: str(round(n, 3)) + '%')
    result['space'] = result['space'].apply(lambda n: str(round(n, 3)) + '%')
    #result.to_csv('pickup_subnew.csv')
    _datautils.to_db(result, 'pickup_subnew')


"""
pickup from industry or concept
"""
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
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma10_space']],
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

def get_warn_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low)


"""
pickup from limitup
"""
def pickup_s2():
    trade = pd.HDFStore('../data/trade.h5')
    df = trade.select('k_limitup_hist')
    limitupdf = df[(df['code'].str.get(0) != '3')][['code', 'p_change', 'date', 'low']]
    # limitupdf = df[(df.code == '603533') & (df.p_change > 9.9)][['code','p_change','date','low']]
    limitupdf = limitupdf.sort_values('date', ascending=True)
    _datautils.to_db(limitupdf, 'pickup2_limitup')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=3, condition=[180, 1])
    print('limitupcount size: ' + str(len(limitupcount)))

    codes = list(limitupcount['code'])
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount, on='code', how='left')
    bottomdf['lmtspace'] = bottomdf[['price', 'lmtuplow']].apply(get_limitup_space, axis=1)
    bottomdf['warn'] = bottomdf[['lmtspace', 'space']].apply(get_warn_space, axis=1)
    print('bottomdf size: ' + str(len(bottomdf)))

    codes = list(bottomdf['code'])
    # 3.ma data
    madf = maup.get_ma(codes)
    # print(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma10_space']], on='code', how='left')
    result = result.sort_values(['space', 'lmtuplow'], axis=0, ascending=[True, True], inplace=False, kind='quicksort',
                                na_position='last')

    #format
    result['change'] = result['change'].apply(lambda n: str(round(n, 2)) + '%')
    # result['space'] = result['space'].apply(lambda n: str(round(n, 2)) + '%')
    # result['lmtspace'] = result['lmtspace'].apply(lambda n: str(round(n, 2)) + '%')

    # save
    result.to_csv('pickup2.csv')
    _datautils.to_db(result, 'pickup2')

    wavecodes = list(result['code'])
    # # get wave data
    # wavedf = wave.get_wave(wavecodes[len(wavecodes) - 20 :]) #get 20
    wavedf = wave.get_wave(wavecodes)  # get all
    #wavedf.to_csv('pickup2_wave.csv')
    _datautils.to_db(wavedf, 'pickup2_wave')

    # # figure display
    # listdf = []
    for code in wavecodes:
        listdf = []
        wdf = wavedf[wavedf.code == code]
        listdf.append(wave.format_wave_data(wdf))
        wave.plot_wave(listdf, filename='./wave/' + code + '.png')

if __name__ == '__main__':
    pickup_subnew_issue_space()
    # pickup_subnew()
    # bottomdf = falco.get_monitor('002852')
    # print(bottomdf)
    # exit()
    #pickup_s2()
    #pickup_s1('i', '零售.txt')




