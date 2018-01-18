import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as _dt

trade = pd.HDFStore('../data/trade.h5', complevel=9, complib='blosc')


def append_newest_record():
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
            print('    insert successfully, total size: ' + str(size))
            # update latest tade
            if '/latest' in keys:
                latestdf = trade.get('latest')
                latest = latestdf[latestdf.date == todaystr]
                if latest.empty:
                    trade.put('latest', todaydf)
                    print('    latest trade data update')
                else:
                    print('    latest trade data existed already')
            else:
                trade.put('latest', todaydf)

            todaydf = histdf[histdf.date == todaystr]
            if todaydf.empty == False:
                print('    hist trade data existed already')
                break

            trade.append('hist', todaydf)

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
    append_newest_record()