import datetime

import numpy as np
import pandas as pd

import tushare as ts
from stocks.base.logging import logger
import stocks.base.dbutils as _dt
from stocks.app import _dateutil


today = _dateutil.get_today()
last_week_start = _dateutil.get_last_week_start()
last_2month_start = _dateutil.get_last_2month_start()
last_year_start = _dateutil.get_last_year_start()


def basics_to_csv():
    basics = ts.get_stock_basics()
    basics['code'] = basics.index
    basics.to_csv('../data/basics.csv', encoding='utf-8')
    _dt.to_db(basics, tbname='basics')


def basics_to_hdf5():
    fundamental = pd.HDFStore('fundamental.h5')
    data = ts.get_stock_basics()
    data['code'] = data.index
    fundamental.put('basics', data)
    fundamental.close()


def hist_volume_to_csv():
    from stocks.data import _datautils
    basics = _datautils.get_basics(excludeCyb=False)
    day_df = pd.DataFrame(columns=['code', 'date', 'open', 'high', 'low', 'close', 'volume'])
    week_df = pd.DataFrame(columns=['code', 'date', 'open', 'high', 'low', 'close', 'volume'])
    month_df = pd.DataFrame(columns=['code', 'date', 'open', 'high', 'low', 'close', 'volume'])
    for index, row in basics.iterrows():
        k_data_day = ts.get_k_data(index, start=last_week_start, end=today)
        k_data_week = ts.get_k_data(index, start=last_2month_start, end=today, ktype='W')
        k_data_month = ts.get_k_data(index, start=last_year_start, end=today, ktype='M')
        if k_data_day is not None and len(k_data_day) > 1:
            day_df = day_df.append(k_data_day[['code', 'date', 'open', 'high', 'low', 'close', 'volume']], ignore_index=True)
        if k_data_week is not None and len(k_data_week) > 0:
            week_df = week_df.append(k_data_week[['code', 'date', 'open', 'high', 'low', 'close', 'volume']], ignore_index=True)
        if k_data_month is not None and len(k_data_month) > 0:
            month_df = month_df.append(k_data_month[['code', 'date', 'open', 'high', 'low', 'close', 'volume']], ignore_index=True)

    _dt.to_db(day_df, tbname='hist_k_day')
    _dt.to_db(week_df, tbname='hist_k_week')
    _dt.to_db(month_df, tbname='hist_k_month')


if __name__ == '__main__':
    logger.info('get basic data start')

    logger.info('etl basic data successfully')
