# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from stocks.util import date_util
from stocks.util.pro_util import pro


def init_trade_date_list():
    '''
    exchange: 交易所 SSE上交所 SZSE深交所
    cal_date: 日历日期
    is_open: 是否交易 0=休市 1=交易
    :return:
    '''
    curt_date = date_util.now().strftime(date_util.FORMAT_FLAT)
    result_df = pro.trade_cal(start_date='20180101', end_date=curt_date)
    result_df = result_df.sort_values('cal_date', ascending=False)
    result_df['hist_date'] = result_df['cal_date'].apply(lambda x: date_util.parse_date_str(x, date_util.FORMAT_DEFAULT))
    result_df = result_df.reset_index()
    result_df.to_csv("hist_trade_date.csv")


def collect_trade_date(n=0):
    hist_date_df = date_util.hist_date_list
    target_date = (date_util.now() + timedelta(days=n)).strftime(date_util.FORMAT_DEFAULT)
    target_df = hist_date_df[hist_date_df.hist_date == target_date]

    if target_df.empty is True:
        start_date = hist_date_df.head(1).loc[0, 'cal_date']
        end_date = (date_util.now() + timedelta(days=n)).strftime(date_util.FORMAT_FLAT)
        result_df = pro.trade_cal(start_date=start_date, end_date=end_date)
        result_df = result_df.sort_values('cal_date', ascending=False)
        result_df['hist_date'] = result_df['cal_date'].apply(
            lambda x: date_util.parse_date_str(x, date_util.FORMAT_DEFAULT))
        hist_date_df = result_df.append(hist_date_df, ignore_index=True, sort=False)
        print(hist_date_df.head(3))
        hist_date_df.to_csv('hist_trade_date.csv')
    else:
        print('collect_trade_date %s existed!' % target_date)


if __name__ == '__main__':
    init_trade_date_list()
    # collect_trade_date(7)
    print('collect_trade_date %s finished!' % date_util.get_today())
