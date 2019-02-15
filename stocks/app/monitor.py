import os
import pandas as pd

import tushare as ts
from stocks.app import falco
from stocks.data import data_util

pd.set_option('display.width', 600)
pd.set_option('precision', 3)

# df = _datautils.get_subnew()
# df = _datautils.filter_cyb(df)
df = data_util.get_data('../data/app/monitormy.txt', sep=' ')
codes = list(df['code'])

if __name__ == '__main__':
    df = falco.get_monitor(codes)
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['price'] = df['price'].apply(lambda x: str(round(float(x), 2)))
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['bottom'] = df['bottom'].apply(lambda x: '[' + str(x) + ']')
    df['space'] = df['space'].apply(lambda x: str(round(x, 2)) + '%')
    print(df[['warn', 'code', 'name', 'change', 'price', 'low', 'high', 'bottom', 'space', 'industry', 'area', 'pe']])
