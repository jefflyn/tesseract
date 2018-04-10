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
from stocks.gene import upnday
from stocks.data.concept import constants as CCONTS
from stocks.data.industry import constants as ICONTS

pd.set_option('display.width', 2000)
pd.set_option('max_columns', 50)
pd.set_option('max_rows', 300)

today = dt.now()
LIMITUP = 'limitup'
BOTTOM = 'bottom'
UPNDAY = 'upnday'
MAUP = 'maup'
QUATO_WEIGHT = {
    LIMITUP: 0.4,
    BOTTOM: 0.3,
    UPNDAY : 0.2,
    MAUP : 0.1
}


"""
return specific subnew code list
fromTime: yyyymmdd
"""
def select_subnew(fromTime=20170409, fname=''):
    subnewbasic = _datautils.get_subnew(marketTimeFrom=fromTime)
    codes = list(subnewbasic['code'])
    result = select_result(codes, filename=fname)
    # print(result)

def select_concepts(name, fname=''):
    data = _datautils.get_stock_data(type='c', filename=name)
    codes = list(data['code'])
    result = select_result(codes, filename=fname)
    # print(result)

def select_industry(name, fname=''):
    data = _datautils.get_stock_data(type='i', filename=name)
    codes = list(data['code'])
    result = select_result(codes, filename=fname)
    # print(result)


def select_xxx(fname=''):
    codes = _datautils.get_app_codes()
    result = select_result(codes, filename=fname)


"""
latest select info 
"""
def select_result(codes, filename=''):
    df = ts.get_realtime_quotes(codes)
    data_list = []
    wavedfset = pd.DataFrame(columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'change'])

    # l1 = pd.DataFrame()
    # l2 = pd.DataFrame()
    for index, row in df.iterrows():
        code = row['code']
        open = float(row['open'])
        current_price = float(row['price'])
        # maybe in trading halt or others situation, ignore this code
        if open <= 0 or current_price <= 0:
            continue;

        basic = _datautils.get_basics(code, True)
        curt_data = []
        curt_data.append(code)
        curt_data.append(row['name'])
        curt_data.append(basic.ix[code, 'industry'])
        curt_data.append(basic.ix[code, 'area'])
        curt_data.append(basic.ix[code, 'pe'])
        curt_data.append(current_price)

        # get wave data and bottom top
        wavedf = wave.get_wave(code) # need to save
        wavestr = wave.wave_to_str(wavedf)
        wavedfset = wavedfset.append(wavedf)
        bottomdf = wave.get_bottom(wavedf)
        bottom = bottomdf.ix[0, 'bottom']
        top = bottomdf.ix[0, 'top']
        uspace = (current_price - bottom) / bottom * 100
        dspace = (current_price - top) / top * 100
        position = (current_price - bottom) / (top - bottom) * 100

        curt_data.append(wavestr)
        curt_data.append(bottom)
        curt_data.append(round(uspace, 2))
        curt_data.append(round(dspace, 2))
        curt_data.append(round(top, 2))

        curt_data.append(round(position, 2))
        curt_data.append(round(bottomdf.ix[0, 'buy1'], 2))
        curt_data.append(round(bottomdf.ix[0, 'buy2'], 2))
        curt_data.append(round(bottomdf.ix[0, 'buy3'], 2))

        # limit up data
        limitupdf = limitup.get_limitup_from_hist_k(code)
        limitupdf = limitup.get_limitup_from_hist_trade(code) if limitupdf.empty == True else limitupdf

        # l1 = l1.append(lupdf, ignore_index=True)
        # l2 = l2.append(limitupdf, ignore_index=True)

        lupcount = 0
        lupcount30 = 0
        lupcountq1 = 0
        lupcountq2 = 0
        lupcountq3 = 0
        lupcountq4 = 0
        lup_lastday = "-"
        luplow = 0
        luphigh = 0
        lupcountdf = limitup.count(limitupdf)
        if lupcountdf.empty == False:
            lupcount = lupcountdf.ix[0, 'count']
            lupcount30 = lupcountdf.ix[0, 'count_30d']
            lupcountq1 = lupcountdf.ix[0, 'count_q1']
            lupcountq2 = lupcountdf.ix[0, 'count_q2']
            lupcountq3 = lupcountdf.ix[0, 'count_q3']
            lupcountq4 = lupcountdf.ix[0, 'count_q4']
            lup_lastday = lupcountdf.ix[0, 'maxdate']
            luplow = lupcountdf.ix[0, 'lup_low']
            luphigh = lupcountdf.ix[0, 'lup_high']

        curt_data.append(lupcount)
        curt_data.append(lupcount30)
        curt_data.append(lupcountq1)
        curt_data.append(lupcountq2)
        curt_data.append(lupcountq3)
        curt_data.append(lupcountq4)
        curt_data.append(lup_lastday)
        curt_data.append(luplow)
        curt_data.append(luphigh)

        # up n day data
        upndaydf = upnday.get_upnday(code)
        updays = 0
        sumup = 0
        ismulti = False
        if upndaydf.empty == False:
            updays = upndaydf.ix[0, 'updays']
            sumup = upndaydf.ix[0, 'sumup']
            ismulti = upndaydf.ix[0, 'multi_vol']
        curt_data.append(updays)
        curt_data.append(sumup)
        curt_data.append(ismulti)

        # get maup data
        maupdf = maup.get_ma(code)
        curt_data.append(maupdf.ix[0, 'isup'])
        curt_data.append(maupdf.ix[0, 'ma5'])
        curt_data.append(maupdf.ix[0, 'ma10'])
        curt_data.append(maupdf.ix[0, 'ma20'])
        curt_data.append(maupdf.ix[0, 'ma30'])
        curt_data.append(maupdf.ix[0, 'ma60'])
        curt_data.append(maupdf.ix[0, 'ma90'])
        curt_data.append(maupdf.ix[0, 'ma120'])
        curt_data.append(maupdf.ix[0, 'ma250'])

        data_list.append(curt_data)
    columns = ['code', 'name', 'industry', 'area', 'pe', 'price', 'wave', 'bottom', 'uspace','dspace', 'top', 'position', 'buy1', 'buy2', 'buy3',
               'count', 'count_30d', 'count_q1', 'count_q2', 'count_q3', 'count_q4', 'maxdate', 'lup_low', 'lup_high',
               'updays', 'sumup', 'multi_vol', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250']
    resultdf = pd.DataFrame(data_list, columns=columns)
    resultdf = resultdf.sort_values('uspace', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    # _datautils.to_db(l1, 'limitup_hist')
    # _datautils.to_db(l2, 'limitup_quota')

    result_name = 'select_result_' + filename
    _datautils.to_db(resultdf, result_name)
    resultdf.to_csv(result_name + '.csv')
    # _datautils.to_db(wavedfset, 'select_wave_' + filename)
    # wavedfset.to_csv('select_wave.csv')

    print("stock selection finish...")
    return resultdf

def score_limitup():
    return QUATO_WEIGHT.get('limiup')

def score_bottom(bspace):
    return 5

def score_upndays(days):
    return 5

def score_maup(malist):
    return 0


def select_subnew_issue_space():
    starttime = dt.now()
    days = datetime.timedelta(-99)
    startstr = dt.strftime(starttime + days, '%Y-%m-%d')

    subnewbasic = _datautils.get_subnew()
    codes = list(subnewbasic['code'])
    # codes = ['601108']
    # get the bottom price data
    df = ts.get_realtime_quotes(codes)
    subnewbasic = subnewbasic.set_index('code')

    rowsize = df.index.size
    data_list = []
    for index, row in df.iterrows():
        print(rowsize - index)
        code = row['code']
        current_price = float(row['price'])
        timeToMarket = subnewbasic.ix[code, 'timeToMarket']
        if timeToMarket == 0 or current_price <= 0:
            continue;
        timeToMarket = str(timeToMarket)
        timeToMarket = timeToMarket[0:4] + '-' + timeToMarket[4:6] + '-' + timeToMarket[6:8]
        issuedays = (starttime - dt.strptime(timeToMarket, '%Y-%m-%d')).days

        firstData = _datautils.get_k_data(code, start=timeToMarket, end=timeToMarket)
        issue_close_price = float(firstData.ix[0, 'close'])
        issue_space = (current_price - issue_close_price) / issue_close_price * 100

        hist99 = _datautils.get_k_data(code, start=startstr)
        if hist99 is None:
            continue
        # var = hist99.var()['close']
        std = hist99.std()['close']
        avg = hist99.mean()['close']
        # varrate = var / avg * 100
        stdrate = std / avg * 100

        curt_data = []
        curt_data.append(code)
        curt_data.append(row['name'])
        curt_data.append(subnewbasic.ix[code, 'industry'])
        curt_data.append(subnewbasic.ix[code, 'area'])
        curt_data.append(subnewbasic.ix[code, 'pe'])

        curt_data.append(issuedays)
        curt_data.append(issue_close_price)
        curt_data.append(current_price)
        curt_data.append(round(issue_space, 2))
        curt_data.append(round(avg, 2))
        # curt_data.append(var)
        curt_data.append(round(std, 2))
        # curt_data.append(varrate)
        curt_data.append(round(stdrate, 2))

        data_list.append(curt_data)
    columns = ['code', 'name','industry','area','pe','liquid_assets','total_assets', 'issue_days', 'issue_price', 'current_price', 'issue_space', 'avg_99', 'std_99', 'stdrate']
    resultdf = pd.DataFrame(data_list, columns=columns)

    resultdf = resultdf.sort_values('issue_space', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
    resultdf['rank'] = [i+1 for i in range(resultdf.index.size)]
    _datautils.to_db(resultdf, 'select_subnew_issue_space' + startstr)
    resultdf['issue_space'] = resultdf['issue_space'].apply(lambda x: str(round(x, 2)) + '%')
    # resultdf['varrate'] = resultdf['varrate'].apply(lambda x: str(round(x, 2)) + '%')
    resultdf['stdrate'] = resultdf['stdrate'].apply(lambda x: str(round(x, 2)) + '%')
    resultdf.to_csv('select_subnew_issue_space.csv')

    wavedf = wave.get_wave(list(resultdf['code']))
    _datautils.to_db(wavedf, 'wave_subnew')



"""
select from industry or concept
"""
def select_s1(type='', classname=''):
    data = _datautils.get_stock_data(type=type, filename=classname)
    codes = list(data['code'])
    limitupdf = limitup.get_limitup_from_hist_k(codes)
    _datautils.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=0, condition=[90,0])
    # print(limitupcount)

    codes = list(limitupcount.index.get_values())
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount[['code', 'count']], on='code', how='left')
    # print(bottomdf)

    # 3.ma data
    madf = maup.get_ma(codes)
    # print(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma10_space']],
                      on='code', how='left')
    result.to_csv('select1.csv')
    _datautils.to_db(result, 'select1')
    # exit()

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
    wave.plot_wave(listdf, filename='select1.png')

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
select from limitup
"""
def select_s2():
    trade = pd.HDFStore('../data/trade.h5')
    df = trade.select('k_limitup_hist')
    limitupdf = df[(df['code'].str.get(0) != '3')][['code', 'p_change', 'date', 'low']]
    # limitupdf = df[(df.code == '603533') & (df.p_change > 9.9)][['code','p_change','date','low']]
    limitupdf = limitupdf.sort_values('date', ascending=True)
    _datautils.to_db(limitupdf, 'select2_limitup')
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
    result.to_csv('select2.csv')
    _datautils.to_db(result, 'select2')

    wavecodes = list(result['code'])
    # # get wave data
    # wavedf = wave.get_wave(wavecodes[len(wavecodes) - 20 :]) #get 20
    wavedf = wave.get_wave(wavecodes)  # get all
    _datautils.to_db(wavedf, 'select2_wave')

    # # figure display
    # listdf = []
    for code in wavecodes:
        listdf = []
        wdf = wavedf[wavedf.code == code]
        listdf.append(wave.format_wave_data(wdf))
        wave.plot_wave(listdf, filename='./wave/' + code + '.png')

def selecttest():
    print(select_result('603083'))

if __name__ == '__main__':
    print('select start...')
    # selecttest()
    # select_xxx('xxx')
    select_subnew(fromTime=20171009, fname='subnew')
    # select_concepts(CCONTS.JYYC, 'jyyc')
    # select_concepts(CCONTS.RGZN, 'rgzn')
    # select_industry(ICONTS.GKHY, 'GKHY')
    # select_subnew_issue_space()
    # select_subnew()
    # bottomdf = falco.get_monitor('002852')
    # print(bottomdf)
    print('select finish...')






