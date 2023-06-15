import datetime

import pandas as pd
import tushare as ts

import zillion.future.db_util as _dt
from zillion.stock.data import data_util
from zillion.utils import date_util as _dateutil

basics = data_util.get_basics(cyb=False)
today = _dateutil.get_today()
this_week_start = _dateutil.get_this_week_start()
last_month_start = _dateutil.get_last_month_start()
last_2month_start = _dateutil.get_last_2month_start()
last_year_start = _dateutil.get_last_year_start()

hist_k_day = data_util.get_hist_k()
hist_k_week = data_util.get_hist_k('W')
hist_k_month = data_util.get_hist_k('M')


def get_period_change(period_k=None):
    """
    including price change, volume change
    :param period_k:
    :return:
    """
    first = period_k.head(1)
    last = period_k.tail(1)
    last_begin_open = first.ix[first.index.to_numpy()[0], 'open'] if (first is not None and len(first) > 0) else 0
    last_end_close = last.ix[last.index.to_numpy()[0], 'close'] if (last is not None and len(last) > 0) else 0
    last_change = 0
    if last_begin_open > 0:
        last_change = (last_end_close - last_begin_open) / last_begin_open * 100

    last_begin_vol = first.ix[first.index.to_numpy()[0], 'volume'] if (first is not None and len(first) > 0) else 0
    last_end_vol = last.ix[last.index.to_numpy()[0], 'volume'] if (last is not None and len(last) > 0) else 0
    vol_change = 0
    if last_begin_vol > 0:
        vol_change = last_end_vol / last_begin_vol

    if vol_change == 1:
        vol_change = last_end_vol
    return [round(last_change, 2), round(vol_change, 2)]


"""
get last 8 statistics by default
"""


def period_statis(period=-6, ktype=None, db_name='change_week_statis'):
    print('start period statistics...')
    result_list = []
    date_pairs = _dateutil.get_trade_day(period)
    columns = None
    if ktype == 'M':
        date_pairs = [monthday for monthday in _dateutil.get_month_firstday_lastday()]
    elif ktype == 'W':
        date_pairs = [_dateutil.get_week_firstday_lastday(w) for w in range(period, 0)]

    date_columns = [d[1] for d in date_pairs]
    new_date_columns = []
    for col in date_columns:
        new_date_columns.append(col)
        new_date_columns.append(col + '_vol')
    columns = ['code', 'name', 'industry', 'area', 'market_time'] + new_date_columns

    for index, row in basics.iterrows():
        markettime = str(row['timeToMarket'])  # exclude new stock by 2 months
        if markettime > last_2month_start:
            continue
        target_k_data = None
        if ktype == 'M':
            target_k_data = hist_k_month[hist_k_month.code == index]
        elif ktype == 'W':
            target_k_data = hist_k_week[hist_k_week.code == index]
        else:
            target_k_data = hist_k_day[hist_k_day.code == index]
        if target_k_data is None or len(target_k_data) == 0:
            continue

        rec_list = []
        rec_list.append(row['code'])
        rec_list.append(row['name'])
        rec_list.append(row['industry'])
        rec_list.append(row['area'])
        rec_list.append(markettime)
        # print(row['code'])

        for targetdate in date_pairs:
            kdata = target_k_data[(target_k_data.date >= targetdate[0]) & (target_k_data.date <= targetdate[1])]
            if kdata is None or len(kdata) < 5:
                kdata = ts.get_k_data(index, start=last_2month_start, end=today, ktype=ktype)
                kdata = kdata[(kdata.date >= targetdate[0]) & (kdata.date <= targetdate[1])]
            change = get_period_change(kdata)
            rec_list.append(change[0])
            rec_list.append(change[1])
        result_list.append(rec_list)
        # break
    print(len(result_list))
    result_df = pd.DataFrame(result_list, columns=columns)
    result_df = result_df.sort_values(columns[-1], ascending=False)
    _dt.to_db(result_df, db_name)
    print('period statistics finished!')


"""
get daily multi volume zillion
"""


def multi_volume_appear():
    start_time = datetime.datetime.now()
    print('multi_volume_appear start...')
    result_list = []

    hist_vol = data_util.get_hist_k()
    for index, row in basics.iterrows():
        markettime = str(row['timeToMarket'])  # exclude new stock
        lastmonth = _dateutil.get_last_month_start('%Y%m%d')
        if markettime > lastmonth:
            continue
        target_k_data = hist_vol[hist_vol.code == index]
        if target_k_data is None:
            target_k_data = ts.get_k_data(index, start=this_week_start, end=today)
        if len(target_k_data) < 2:
            continue

        rec_list = []
        rec_list.append(row['code'])
        rec_list.append(row['name'])
        rec_list.append(row['industry'])
        rec_list.append(row['area'])
        rec_list.append(markettime)

        index_list = target_k_data.index.to_numpy()
        pre_vol = target_k_data.ix[index_list[-2], 'volume']
        nxt_vol = target_k_data.ix[index_list[-1], 'volume']
        vol_rate = nxt_vol / pre_vol
        rec_list.append(round(vol_rate, 2))

        pre_close = target_k_data.ix[index_list[-2], 'close']
        nxt_close = target_k_data.ix[index_list[-1], 'close']
        rec_list.append(round((nxt_close - pre_close) / pre_close * 100, 2))
        result_list.append(rec_list)
    print(len(result_list))
    result_df = pd.DataFrame(result_list,
                             columns=['code', 'name', 'industry', 'area', 'market_time', 'vol_rate', 'change'])

    result_df = result_df.sort_values('vol_rate', ascending=False)
    _dt.to_db(result_df, 'change_statis_volume')
    print('multi_volume_appear end!')


def period_statis_from_hist():
    print('period_statis_from_hist start...')
    result = []
    for index, row in basics.iterrows():
        markettime = str(row['timeToMarket'])  # exclude new stock by 2 months
        if markettime > last_2month_start:
            continue
        hist_data = ts.get_hist_data(code=index, ktype='W')
        result.append(hist_data)
    print(len(result))
    print('period_statis_from_hist end!')


def change_statis_month():
    df = _dt.read_query('select code, date, p_change from hist_change_month')
    change_statis = df.pivot(index='code', columns='date', values='p_change')
    change_statis.insert(0, 'code', change_statis.index)
    columns = change_statis.columns
    change_statis = change_statis.sort_values(by=columns[-1], ascending=False)
    _dt.to_db(change_statis, 'hist_change_month_statis')
    print('finished!')


def change_statis_week():
    df = _dt.read_query('select code, date, p_change from hist_change_week')
    change_statis = df.pivot(index='code', columns='date', values='p_change')
    change_statis.insert(0, 'code', change_statis.index)
    columns = change_statis.columns
    change_statis = change_statis.sort_values(by=columns[-1], ascending=False)
    _dt.to_db(change_statis, 'hist_change_week_statis')
    print('finished!')


if __name__ == '__main__':
    print('start main')
    change_statis_week()
    change_statis_month
    # period_statis_from_hist()
    # period_statis(ktype='M', db_name='change_statis_month')
    # period_statis(period=-4, ktype='W', db_name='change_statis_week')
    # period_statis(period=-5, ktype='D', db_name='change_statis_day')
    # multi_volume_appear()
