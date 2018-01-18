import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils

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


if __name__ == '__main__':
    basics_to_csv()
    basics_to_hdf5()
    print(str(datetime.datetime.now()) + ': etl basic data successfully')