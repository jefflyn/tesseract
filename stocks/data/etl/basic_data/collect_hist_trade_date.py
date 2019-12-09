# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

import pandas as pd
import tushare.util.dateu as ts_dateu
from datetime import timedelta
from stocks.util.logging import logger
from stocks.util import date_util


def init_trade_date_list():
    n = 0
    result = list()
    while True:
        target_date = (date_util.get_now() - timedelta(days=n)).strftime(date_util.default_format)
        query_date = date_util.convert_to_date(query_date)
        is_holiday = ts_dateu.is_holiday(query_date)
        if is_holiday is False:
            date_list = [target_date, 1]
        else:
            date_list = [target_date, 0]
        result.append(date_list)
        print(date_list)

        n += 1
        if n == 3650:
            break
    result_df = pd.DataFrame(result, columns=['hist_date', 'is_trade'])
    print(result_df)
    # result_df.to_csv("hist_trade_date.csv")


def collect_trade_date():
    target_date = date_util.get_today()
    hist_date_df = date_util.hist_date_list
    target_df = hist_date_df[hist_date_df.hist_date == target_date]
    if target_df.empty is True:
        query_date = date_util.convert_to_date(target_date)
        is_holiday = ts_dateu.is_holiday(query_date)
        if is_holiday is False:
            date_list = [target_date, 1]
        else:
            date_list = [target_date, 0]
        insert_df = pd.DataFrame([date_list], columns=['hist_date', 'is_trade'])
        hist_date_df = insert_df.append(hist_date_df, ignore_index=True, sort=False)
        hist_date_df = hist_date_df[['hist_date', 'is_trade']]
        print(hist_date_df.head(10))
        hist_date_df.to_csv('hist_trade_date.csv')
    else:
        logger.info('collect_trade_date %s existed!' % date_util.get_today())


if __name__ == '__main__':
    collect_trade_date()
    logger.info('collect_trade_date %s finished!' % date_util.get_today())
