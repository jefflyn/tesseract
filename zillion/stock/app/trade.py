import datetime
import time

import akshare
import pandas as pd

from zillion.utils import date_util
from zillion.utils.date_util import now_str, today

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def format_realtime(df):
    """
    格式化数据
    :param df:
    :return:
    """
    df['涨跌幅'] = df['涨跌幅'].map(str) + '%'
    df = df.drop(columns=['序号'])
    return df


def hist():
    print(akshare.stock_us_hist())
    print(akshare.stock_us_daily())


def us_realtime(code=None):
    print(akshare.stock_us_spot_em())
    print(akshare.stock_us_spot())


def hk_realtime_em(code=None):
    df = akshare.stock_hk_spot_em()
    # df['time'] = date_util.now_str()
    # db_stock.to_db(df, 'basic_hk')
    if code is not None:
        df = df[df['代码'].isin(code)]
    return format_realtime(df)


def hk_realtime_mb_em(code=None):
    df = akshare.stock_hk_main_board_spot_em()
    if code is not None:
        df = df[df['代码'].isin(code)]
    return format_realtime(df)


def hk_realtime_sn(code=None):
    df = akshare.stock_hk_spot()
    # db_stock.to_db(df, 'basic_hk_sn')
    if code is not None:
        df = df[df['symbol'].isin(code)]
    return df


if __name__ == '__main__':
    open_time = datetime.datetime(today.year, today.month, today.day, hour=16, minute=30, second=30)
    while True:
        print(hk_realtime_em(['00700', '09988', '03690', '09999', '09888',
                              '09618', '01810', '02015', '01024', '09961']))
        print('time:', now_str())
        time.sleep(5)
        if date_util.now() > open_time:
            break
    # print(hk_realtime_sn(['09988']))
