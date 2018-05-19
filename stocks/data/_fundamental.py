import datetime

import numpy as np
import pandas as pd

import tushare as ts
from stocks.data import _datautils
from stocks.app import _dateutil


today = _dateutil.get_today()
last_week_start = _dateutil.get_last_week_start()



def basics_to_csv():
    basics = ts.get_stock_basics()
    basics['code'] = basics.index
    basics.to_csv('../data/basics.csv', encoding='utf-8')
    _datautils.to_db(basics, tbname='basics')


def basics_to_hdf5():
    fundamental = pd.HDFStore('fundamental.h5')
    data = ts.get_stock_basics()
    data['code'] = data.index
    fundamental.put('basics', data)
    fundamental.close()


def hist_volume_to_csv():
    basics = _datautils.get_basics(excludeCyb=False)
    init_df = pd.DataFrame(columns=['code', 'date', 'open', 'close', 'volume'])
    for index, row in basics.iterrows():
        target_k_data = ts.get_k_data(index, start=last_week_start, end=today)
        if target_k_data is None or len(target_k_data) < 2:
            continue
        init_df = init_df.append(target_k_data[['code', 'date', 'open', 'close', 'volume']], ignore_index=True)

    # print(init_df)
    init_df.to_csv('../data/hist_volume.csv', encoding='utf-8')
    _datautils.to_db(init_df, tbname='hist_volume'+today)


if __name__ == '__main__':
    print('get basic data start', datetime.datetime.now())
    basics_to_csv()
    basics_to_hdf5()
    hist_volume_to_csv()
    print('etl basic data successfully', datetime.datetime.now())