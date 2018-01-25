import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as _dt

trade = pd.HDFStore('../data/trade.h5', complevel=9, complib='blosc')
trade_k = pd.HDFStore('../data/trade_k.h5', complevel=9, complib='blosc')


def append_hist_k_limitup_record():
    # trade.remove('latest')
    today = datetime.today()
    todaystr = datetime.strftime(today, '%Y-%m-%d')
    histdf = trade.get('hist')
    keys = trade.keys()
    oneday = dt.timedelta(-1)
    targetdatestr = todaystr
    while True:
        print(targetdatestr + ' get trade data >>>')
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
                    print('    latest trade data update')
                else:
                    print('    latest trade data existed already')
            else:
                trade.put('latest', todaydf)

            targetdf = histdf[histdf.date == targetdatestr]
            if targetdf.empty == False:
                print('    hist trade data existed already')
                break

            trade.append('hist', todaydf)
            print('    insert successfully, total size: ' + str(size))
        except Exception as e:
            print('    ' + str(e))

        today = today + oneday
        targetdatestr = datetime.strftime(today, '%Y-%m-%d')

    trade.close()


def get_hist_k_limitup_date():
    startdate = None
    oneday = dt.timedelta(-1)
    i = 0
    today = datetime.today() if startdate == None else datetime.strptime(startdate, '%Y-%m-%d')
    todaystr = datetime.strftime(today, '%Y-%m-%d') if startdate == None else startdate
    while todaystr > '2017-06-13':
        try:
            print(todaystr + ' get trade data >>>')
            i = i + 1
            todaydf = _dt.get_totay_quotations(todaystr)
            todaydf = todaydf[todaydf.p_change > 9.9]
            size = len(todaydf.index.get_values())
            print('    total size: ' + str(size))

            for index, row in todaydf.iterrows():
                code = row['code']
                change = row['p_change']

                hist_k = ts.get_k_data(code, start=todaystr, end=todaystr)
                hist_k['p_change'] = change

                trade.append('k_limitup_hist', hist_k)
                print('    append hist k data')
        except Exception as e:
            print('    ' + str(e))
        today = today + oneday
        todaystr = datetime.strftime(today, '%Y-%m-%d')

    trade.close()


"""
暂时不用
"""
def get_hist_k_code():
    todaydf = _dt.get_totay_quotations('2018-01-24')
    codes = list(todaydf['code'])

    index = 0
    for code in codes:
        hist_k = ts.get_k_data(code, start='2016-01-24')
        trade_k.put(code, hist_k)
        index = index + 1
        print(str(index) + ' ' + code)

    trade_k.close()


def append_newest_record():
    # trade.remove('latest')
    today = datetime.today()
    todaystr = datetime.strftime(today, '%Y-%m-%d')
    histdf = trade.get('hist')
    keys = trade.keys()
    oneday = dt.timedelta(-1)
    targetdatestr = todaystr
    while True:
        print(targetdatestr + ' get trade data >>>')
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
                    print('    latest trade data update')
                else:
                    print('    latest trade data existed already')
            else:
                trade.put('latest', todaydf)

            targetdf = histdf[histdf.date == targetdatestr]
            if targetdf.empty == False:
                print('    hist trade data existed already')
                break

            trade.append('hist', todaydf)
            print('    insert successfully, total size: ' + str(size))
        except Exception as e:
            print('    ' + str(e))

        today = today + oneday
        targetdatestr = datetime.strftime(today, '%Y-%m-%d')

    trade.close()


def get_hist_trade(startdate=None):
    oneday = dt.timedelta(-1)
    i = 0
    today = datetime.today() if startdate == None else datetime.strptime(startdate, '%Y-%m-%d')
    todaystr = datetime.strftime(today, '%Y-%m-%d') if startdate == None else startdate
    while todaystr > '2017-06-13':
        try:
            print(todaystr + ' get trade data >>>')
            i = i + 1
            todaydf = _dt.get_totay_quotations(todaystr)
            size = len(todaydf.index.get_values())
            print('    total size: ' + str(size))
            #add date col
            dates = [todaystr] * size
            todaydf.insert(0, 'date', dates)

            trade.append('hist', todaydf)
            keys = trade.keys()
            if '/latest' not in keys:
                trade.append('latest', todaydf)
                print('    insert latest trade data')
        except Exception as e:
            print('    ' + str(e))
        today = today + oneday
        todaystr = datetime.strftime(today, '%Y-%m-%d')

    trade.close()


if __name__ == '__main__':
    # get_hist_k_limitup_date()
    append_newest_record()