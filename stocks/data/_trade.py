import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as _dt

trade = pd.HDFStore('../data/trade.h5', complevel=9, complib='blosc')


def get_hist_limitup_data():
    trade.remove('k_limitup_hist')

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
        try:
            print(todaystr + ' get trade data >>>')
            i = i + 1
            todaydf = _dt.get_totay_quotations(todaystr)

            if histdf is not None:
                targetdf = histdf[histdf.date == todaystr]
                if targetdf.empty == False:
                    print('    limitup hist k data existed already')
                    break

            todaydf = todaydf[todaydf.p_change > 9.9]
            size = len(todaydf.index.get_values())


            # limitupdf = pd.DataFrame(columns=['date','open','close','high','low','volume','code','p_change'])
            limitupdf = pd.DataFrame()
            for index, row in todaydf.iterrows():
                code = row['code']
                change = row['p_change']

                hist_k = ts.get_k_data(code, start=todaystr, end=todaystr)
                hist_k['p_change'] = change
                limitupdf = limitupdf.append(hist_k)

            trade.append('k_limitup_hist', limitupdf)
            print('    append limitup hist k data successfully, total size: ' + str(len(limitupdf.index.values)))
        except Exception as e:
            print('    ' + str(e))
        today = today + oneday
        todaystr = datetime.strftime(today, '%Y-%m-%d')



def append_latest_trade():
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


def view_hist_data():
    histdf = trade.get('hist')
    #histdf.to_csv('hist_trade')
    # _dt.to_db(histdf, 'hist_data')

def view_limitup_hist():
    histdf = trade.get('k_limitup_hist')
    _dt.to_db(histdf, 'hist_limitup')


if __name__ == '__main__':
    # view_limitup_hist()

    # append_latest_trade()

    get_hist_limitup_data()

    # get_hist_trade()


    trade.close()