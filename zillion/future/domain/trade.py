import pandas as pd
import requests

from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

option = {'Referer': 'http://finance.sina.com.cn'}
url = 'http://w.sinajs.cn/?list='
sina_prefix = 'nf_'


def _realtime(codes=None):
    codes = (sina_prefix + codes) if isinstance(codes, str) else ','.join([sina_prefix + c for c in codes])
    result_txt = requests.get(url + codes, headers=option).text
    realtime_list = []
    if result_txt is not None and len(result_txt.split(';')) > 0:
        groups = result_txt.split(';\n')
        for content in groups:
            if len(content) == 0:
                continue
            code = content.split('=')[0].split('_')[-1]
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
    return data_df[
        ['code', 'date', 'open', 'high', 'low', 'pre_close', 'close', 'settle', 'pre_settle', 'hold', 'volume']]


def realtime_simple(code=None):
    data_df = _realtime(code)
    return data_df[['code', 'date', 'open', 'high', 'low', 'close', 'bid', 'ask', 'settle', 'pre_settle']]


if __name__ == '__main__':
    df = _realtime('SF0')
    print(df)
    result = _realtime(['PG2403', 'SA2405'])
    print(result)
