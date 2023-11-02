import pandas as pd
import requests

from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

option = {'Referer': 'http://finance.sina.com.cn'}
url = 'http://w.sinajs.cn/?list=nf_'


def _realtime(code=None):
    result = requests.get(url + code, headers=option).text
    realtime_list = []
    if result is not None and len(result.split(';')) > 0:
        groups = result.split(';\n')
        for content in groups:
            if len(content) == 0:
                continue
            info = content.split('=')[1].replace('"', '').strip().split(',')
            if len(info) < 18:
                continue
            pre_close = 0
            trade_date = date_util.parse_date_str(info[17], date_util.FORMAT_FLAT)
            realtime_list.append([code, trade_date, float(info[2]), float(info[3]), float(info[4]),
                                  pre_close, float(info[6]), float(info[7]), float(info[8]), float(info[9]),
                                  float(info[10]), float(info[11]), float(info[12]), float(info[13]), float(info[14])])
    realtime_df = pd.DataFrame(realtime_list, columns=['code', 'date', 'open', 'high', 'low',
                                                       'pre_close', 'bid', 'ask', 'close', 'settle',
                                                       'pre_settle', 'buy_vol', 'sell_vol', 'hold', 'volume'])
    return realtime_df


def realtime_for_daily(code=None):
    data_df = _realtime(code)
    return data_df[['code', 'date', 'open', 'high', 'low', 'pre_close', 'close', 'settle', 'pre_settle', 'hold', 'volume']]


def realtime_simple(code=None):
    result = requests.get(url + code, headers=option).text
    realtime_list = []
    if result is not None and len(result.split(';')) > 0:
        groups = result.split(';\n')
        for content in groups:
            if len(content) == 0:
                continue
            info = content.split('=')[1].replace('"', '').strip().split(',')
            if len(info) < 18:
                continue
            trade_date = date_util.parse_date_str(info[17], date_util.FORMAT_FLAT)
            realtime_list.append([code, trade_date, float(info[2]), float(info[3]), float(info[4]), float(info[8]),
                                  float(info[6]), float(info[7]), float(info[10])])
    realtime_df = pd.DataFrame(realtime_list, columns=['code', 'date', 'open', 'high', 'low', 'close', 'bid', 'ask',
                                                       'pre_settle'])
    return realtime_df


if __name__ == '__main__':
    df = _realtime(code='SF0')
    print(df)
