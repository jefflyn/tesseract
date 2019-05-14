import datetime
import sys
from datetime import datetime as dt
from sys import argv

import pandas as pd
import stocks.base.db_util as _dt
import tushare as ts
from stocks.app import falco
from stocks.base.logging import logger
from stocks.data import data_util
from stocks.base import date_util
from stocks.gene import limitup
from stocks.gene import maup
from stocks.gene import upnday
from stocks.gene import wave
from stocks.base import display

LIMITUP = 'limitup'
BOTTOM = 'bottom'
UPNDAY = 'upnday'
MAUP = 'maup'
QUATO_WEIGHT = {
    LIMITUP: 0.4,
    BOTTOM: 0.3,
    UPNDAY: 0.2,
    MAUP: 0.1
}

latest_trade_date = date_util.get_latest_trade_date(1)[0]


def select_from_change_week():
    change_df = _dt.read_query('select * from hist_change_statis_week')
    columns = change_df.columns
    for col in columns[1::]:
        logger.info('hist_change_statis_week sorted by column %s' % col)
        change_df = change_df.sort_values(by=col, ascending=False)
        target_change = change_df[change_df[col] >= 15.0]
        if target_change is None or target_change.empty is True:
            continue
        codes = list(target_change['code'])
        select_result(codes, filename='week_' + col)
    logger.info('finished!')


def select_from_change_month():
    change_df = _dt.read_query('select * from hist_change_statis_month')
    columns = change_df.columns
    for col in columns[1::]:
        if col != '2018-07':
            continue
        logger.info('hist_change_statis sorted by column %s' % col)
        change_df = change_df.sort_values(by=col, ascending=False)
        target_change = change_df[change_df[col] >= 20.0]
        if target_change is None or target_change.empty is True:
            continue
        codes = list(target_change['code'])
        select_result(codes, filename='month_' + col)
    logger.info('finished!')


def select_from_all(fname='all'):
    """
    select all stocks 
    :param fname: all
    :return: 
    """
    select_result(filename=fname)


def select_from_subnew(from_date=None, fname='subnew'):
    """
    return specific subnew code list
    fromTime: yyyymmdd
    """
    subnew = data_util.get_subnew(list_date=from_date)
    codes = list(subnew['code'])
    select_result(codes, filename=fname)


def merge_select_result():
    return None


def select_result(codeset=None, filename=''):
    trade_date_list = date_util.get_latest_trade_date(3)
    hist_trade_df = None
    for trade_date in trade_date_list:
        hist_trade_df = data_util.get_hist_trade(code=codeset, start=trade_date, end=latest_trade_date)
        if len(hist_trade_df) > 0:
            logger.info('get latest trade: %s' % trade_date)
            break
    size = 0
    if codeset is not None:
        size = len(codeset)
    else:
        size = len(hist_trade_df.index.get_values())
    logger.info('select stocks start! total size: %d\n' % size)
    # limit = 500
    # beginIndex = 0
    # endIndex = beginIndex + limit if size > limit else size
    # logger.info('select from %s, total: %i' % (filename, size))
    data_list = []

    # while endIndex <= size:
    #     logger.info('process from %d to %d' % (beginIndex, endIndex))
    #     codes = codeset[beginIndex: endIndex]
    #     df = ts.get_realtime_quotes(codes)

        # beginIndex = endIndex
        # endIndex = endIndex + limit
    wavedfset = pd.DataFrame(columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'change'])
    for index, row in hist_trade_df.iterrows():
        code = row['code']
        logger.info('count down ' + str(size) + ' >>> processing ' + code)
        size -= 1
        open = float(row['open'])
        current_price = float(row['close'])
        # maybe in trading halt or others situation, ignore this code
        if open <= 0 or current_price <= 0:
            continue

        basic = data_util.get_basics(code)
        if basic is None or basic.empty is True:
            continue
        curt_data = list()
        curt_data.append(code)
        curt_data.append(basic.ix[code, 'name'])
        curt_data.append(basic.ix[code, 'industry'])
        curt_data.append(basic.ix[code, 'area'])
        curt_data.append(basic.ix[code, 'list_date'])
        curt_data.append(current_price)

        # get wave data and bottom top
        wavedf = wave.get_wave(code)  # need to save
        # logger.debug(code)
        wave_size = 5
        if filename == 'subnew':
            wave_size = 10
        wavestr = wave.wave_to_str(wavedf, wave_size)
        wavestr_ab = wavestr.split('\n')[0].split('|')
        wave_a = float(wavestr_ab[-2] if wavestr_ab[-2] != '' else '0')
        wave_b = float(wavestr_ab[-1])
        wavedfset = wavedfset.append(wavedf)
        bottomdf = wave.get_bottom(wavedf)
        if bottomdf is None or bottomdf.empty is True:
            continue
        bottom = bottomdf.ix[0, 'bottom']
        top = bottomdf.ix[0, 'top']
        uspace = (current_price - bottom) / bottom * 100
        dspace = (current_price - top) / top * 100
        position = (current_price - bottom) / (top - bottom) * 100

        curt_data.append(wavestr)
        curt_data.append(round(wave_a, 2))
        curt_data.append(round(wave_b, 2))
        curt_data.append(bottom)
        curt_data.append(round(uspace, 2))
        curt_data.append(round(dspace, 2))
        curt_data.append(round(top, 2))

        curt_data.append(round(position, 2))
        curt_data.append(round(bottomdf.ix[0, 'buy1'], 2))
        curt_data.append(round(bottomdf.ix[0, 'buy2'], 2))
        curt_data.append(round(bottomdf.ix[0, 'buy3'], 2))

        # limit up data
        limitupdf = limitup.get_limitup_from_hist_trade(code)

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
        if lupcountdf.empty is False:
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
        multi_vol_rate = 1
        vol_rate = 0
        change_7_days = ''
        sum_30_days = 0
        gap = 0
        if upndaydf.empty is False:
            change_7_days = upndaydf.ix[0, 'change_7_days']
            gap = upndaydf.ix[0, 'gap']
            sum_30_days = upndaydf.ix[0, 'sum_30_days']
            updays = upndaydf.ix[0, 'updays']
            sumup = upndaydf.ix[0, 'sumup']
            multi_vol_rate = upndaydf.ix[0, 'multi_vol']
            vol_rate = upndaydf.ix[0, 'vol_rate']
        curt_data.append(change_7_days)
        curt_data.append(gap)
        curt_data.append(sum_30_days)
        curt_data.append(updays)
        curt_data.append(sumup)
        curt_data.append(multi_vol_rate)
        curt_data.append(vol_rate)

        # get maup data
        maupdf = maup.get_ma(code)
        curt_data.append(maupdf.ix[0, 'isup'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma5'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma10'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma20'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma30'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma60'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma90'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma120'] if maupdf.empty is False else 0)
        curt_data.append(maupdf.ix[0, 'ma250'] if maupdf.empty is False else 0)

        data_list.append(curt_data)
    columns = ['code', 'name', 'industry', 'area', 'list_date', 'price', 'wave', 'wave_a', 'wave_b', 'bottom', 'uspace%', 'dspace%',
               'top', 'position%', 'buy1', 'buy2', 'buy3',
               'count', 'count_30d', 'count_q1', 'count_q2', 'count_q3', 'count_q4', 'maxdate', 'lup_low', 'lup_high',
               'change_7_days', 'gap', 'sum_30_days', 'updays', 'sumup%', 'multi_vol', 'vol_rate', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90',
               'ma120', 'ma250']
    resultdf = pd.DataFrame(data_list, columns=columns)
    resultdf = resultdf.sort_values('sum_30_days', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')

    resultdf = resultdf[
        ['code', 'name', 'industry', 'area', 'list_date', 'price', 'wave', 'wave_a', 'wave_b', 'bottom', 'uspace%', 'dspace%',
         'top', 'position%', 'gap', 'sum_30_days', 'count', 'count_30d', 'count_q1', 'count_q2', 'count_q3', 'count_q4', 'maxdate', 'lup_low', 'lup_high',
         'buy1', 'buy2', 'buy3', 'change_7_days', 'updays', 'sumup%', 'vol_rate', 'multi_vol',
         'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250']]
    resultdf['select_time'] = dt.now()
    result_name = 'select_result_' + filename
    _dt.to_db(resultdf, result_name)
    _dt.to_db(wavedfset, 'select_wave_' + filename)
    logger.info('select stocks finished! result size: %d\n' % len(resultdf.index.get_values()))
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

    subnewbasic = data_util.get_subnew()
    codes = list(subnewbasic['code'])
    # codes = ['601108']
    # get the bottom price data
    df = ts.get_realtime_quotes(codes)
    subnewbasic = subnewbasic.set_index('code')

    rowsize = df.index.size
    data_list = []
    for index, row in df.iterrows():
        logger.info(rowsize - index)
        code = row['code']
        current_price = float(row['price'])
        timeToMarket = subnewbasic.ix[code, 'timeToMarket']
        if timeToMarket == 0 or current_price <= 0:
            continue;
        timeToMarket = str(timeToMarket)
        timeToMarket = timeToMarket[0:4] + '-' + timeToMarket[4:6] + '-' + timeToMarket[6:8]
        issuedays = (starttime - dt.strptime(timeToMarket, '%Y-%m-%d')).days

        firstData = data_util.get_k_data(code, start=timeToMarket, end=timeToMarket)
        issue_close_price = float(firstData.ix[0, 'close'])
        issue_space = (current_price - issue_close_price) / issue_close_price * 100

        hist99 = data_util.get_k_data(code, start=startstr)
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
    columns = ['code', 'name', 'industry', 'area', 'pe', 'liquid_assets', 'total_assets', 'issue_days', 'issue_price',
               'current_price', 'issue_space', 'avg_99', 'std_99', 'stdrate']
    resultdf = pd.DataFrame(data_list, columns=columns)

    resultdf = resultdf.sort_values('issue_space', axis=0, ascending=True, inplace=False, kind='quicksort',
                                    na_position='last')
    resultdf['rank'] = [i + 1 for i in range(resultdf.index.size)]
    _dt.to_db(resultdf, 'select_subnew_issue_space' + startstr)
    resultdf['issue_space'] = resultdf['issue_space'].apply(lambda x: str(round(x, 2)) + '%')
    # resultdf['varrate'] = resultdf['varrate'].apply(lambda x: str(round(x, 2)) + '%')
    resultdf['stdrate'] = resultdf['stdrate'].apply(lambda x: str(round(x, 2)) + '%')
    resultdf.to_csv('select_subnew_issue_space.csv')

    wavedf = wave.get_wave(list(resultdf['code']))
    _dt.to_db(wavedf, 'wave_subnew')


"""
select from industry or concept
"""


def select_s1(type='', classname=''):
    data = data_util.get_stock_data(type=type, filename=classname)
    codes = list(data['code'])
    limitupdf = limitup.get_limitup_from_hist_k(codes)
    _dt.to_db(limitupdf, 'limitupx')
    # 1.choose the active codes from the limitups which limitup at lease more than n
    limitupcount = limitup.count(limitupdf, times=0, condition=[90, 0])
    # logger.info(limitupcount)

    codes = list(limitupcount.index.get_values())
    # 2.get the bottom price data
    bottomdf = falco.get_monitor(codes)
    bottomdf = pd.merge(bottomdf, limitupcount[['code', 'count']], on='code', how='left')
    # logger.info(bottomdf)

    # 3.ma data
    madf = maup.get_ma(codes)
    # logger.info(madf)
    result = pd.merge(bottomdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma30std', 'ma10_space']],
                      on='code', how='left')
    result.to_csv('select1.csv')
    _dt.to_db(result, 'select1')
    # exit()

    #########
    wavecodes = list(result['code'])
    # 4.get wave data
    wavedf = wave.get_wave(wavecodes)
    # logger.info(wavedf)
    listdf = []
    for code in wavecodes:
        wdf = wavedf[wavedf.code == code]
        listdf.append(wave.format_wave_data(wdf))
    # figure display
    wave.plot_wave(listdf, filename='select1.png')

    # 5.limitup data
    logger.info(limitupdf)


def get_limitup_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low) / low * 100


def get_warn_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low)


def selecttest():
    logger.info(select_result('603083'))


if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
        sys.exit(0)
    codes = argv[1]

    result = select_result(codes)
    # print(result)
