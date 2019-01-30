import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts
import stocks.base.dbutils as dbutils
import stocks.data._datautils as _dt
from stocks.base.logging import logger

# trade = pd.HDFStore('../data/trade.h5', complevel=9, complib='blosc')


def get_hist_limitup_data():
    # trade.remove('k_limitup_hist') # for reset

    logger.info('【get_hist_limitup_data start】...')
    histdf = None
    keys = trade.keys()
    if '/k_limitup_hist' in keys:
        histdf = trade.get('k_limitup_hist')
    startdate = None
    oneday = dt.timedelta(-1)
    i = 0
    today = datetime.today() if startdate == None else datetime.strptime(startdate, '%Y-%m-%d')
    todaystr = datetime.strftime(today, '%Y-%m-%d') if startdate == None else startdate

    while todaystr > '2017-06-13':
        limitupdf = pd.DataFrame(columns=['date', 'open', 'close', 'high', 'low', 'volume', 'code', 'p_change'])
        # limitupdf = pd.DataFrame()
        try:
            print(todaystr + ' get trade data >>>')
            i = i + 1
            todaydf = _dt.get_totay_quotations(todaystr)

            if histdf is not None:
                targetdf = histdf[histdf.date == todaystr]
                if targetdf.empty == False:
                    logger.info('    limitup hist k data existed already')
                    break

            todaydf = todaydf[todaydf.p_change > 9.9]
            size = len(todaydf.index.get_values())

            for index, row in todaydf.iterrows():
                code = row['code']
                change = row['p_change']
                open = row['open']
                close = row['price']
                high = row['high']
                low = row['low']
                volume = row['volume']
                try:
                    hist_k = ts.get_k_data(code)
                    hist_k = hist_k[hist_k.date == todaystr]
                    hist_k['p_change'] = change
                    if hist_k is None or len(hist_k) == 0:
                        quotadata = {'date': todaystr, 'open': open, 'close': close, 'high': high, 'low': low,
                                     'volume': volume, 'code': code, 'p_change': change}
                        hist_k = quotadata
                    limitupdf = limitupdf.append(hist_k, ignore_index=True)
                except Exception as le:
                    quotadata = {'date': todaystr, 'open': open, 'close': close, 'high': high, 'low': low,
                                 'volume': volume, 'code': code, 'p_change': change}
                    limitupdf = limitupdf.append(pd.DataFrame(quotadata), ignore_index=True)
                    logger.info('    ' + str(le) + ', use today quota data')

            trade.append('k_limitup_hist', limitupdf)
            logger.info('    append limitup hist k data successfully, total size: ' + str(len(limitupdf.index.values)))
        except Exception as e:
            logger.info('    ' + str(e))

        today = today + oneday
        todaystr = datetime.strftime(today, '%Y-%m-%d')


"""
append the latest trade data every trade date
"""


def append_latest_trade():
    logger.info('【append_latest_trade start】...')
    # trade.remove('latest')
    today = datetime.today()
    todaystr = datetime.strftime(today, '%Y-%m-%d')
    histdf = trade.get('hist')
    keys = trade.keys()
    oneday = dt.timedelta(-1)
    targetdatestr = todaystr
    while True:
        logger.info(targetdatestr + ' get trade data >>>')
        try:
            todaydf = _dt.get_totay_quotations(targetdatestr)
            size = len(todaydf.index.get_values())
            dates = [targetdatestr] * size
            todaydf.insert(0, 'date', dates)
            # update latest tade
            if '/latest' in keys:
                # trade.remove('latest')
                latestdf = trade.get('latest')
                latestdate = latestdf.at[0, 'date']
                if latestdate < targetdatestr:
                    trade.put('latest', todaydf)
                    logger.info('    latest trade data update')
                else:
                    logger.info('    latest trade data existed already')
            else:
                trade.put('latest', todaydf)

            targetdf = histdf[histdf.date == targetdatestr]
            if targetdf.empty == False:
                logger.info('    hist trade data existed already')
                break

            trade.append('hist', todaydf)
            logger.info('    insert successfully, total size: ' + str(size))
        except Exception as e:
            logger.info('    ' + str(e))

        today = today + oneday
        targetdatestr = datetime.strftime(today, '%Y-%m-%d')


def get_hist_trade(startdate=None):
    oneday = dt.timedelta(-1)
    i = 0
    today = datetime.today() if startdate == None else datetime.strptime(startdate, '%Y-%m-%d')
    todaystr = datetime.strftime(today, '%Y-%m-%d') if startdate == None else startdate
    while todaystr > '2017-06-13':
        try:
            logger.info(todaystr + ' get trade data >>>')
            i = i + 1
            todaydf = _dt.get_totay_quotations(todaystr)
            size = len(todaydf.index.get_values())
            logger.info('    total size: ' + str(size))
            # add date col
            dates = [todaystr] * size
            todaydf.insert(0, 'date', dates)

            trade.append('hist', todaydf)
            keys = trade.keys()
            if '/latest' not in keys:
                trade.append('latest', todaydf)
                logger.info('    insert latest trade data')
        except Exception as e:
            logger.info('    ' + str(e))
        today = today + oneday
        todaystr = datetime.strftime(today, '%Y-%m-%d')


def view_hist_data():
    histdf = trade.get('hist')
    # histdf.to_csv('hist_trade')
    # _dt.to_db(histdf, 'hist_data')


def view_limitup_hist():
    histdf = trade.get('k_limitup_hist')
    dbutils.to_db(histdf, 'hist_limitup')


if __name__ == '__main__':
    get_hist_trade()
    append_latest_trade()
    get_hist_limitup_data()

    # view_hist_data()
    # view_limitup_hist()

    trade.close()
