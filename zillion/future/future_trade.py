import pandas as pd
import requests

from zillion.utils import date_util

option = {'Referer': 'http://finance.sina.com.cn'}
url = 'http://w.sinajs.cn/?list=nf_'


def realtime(code=None):
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
            realtime_list.append([code, trade_date, float(info[2]), float(info[3]), float(info[4]), float(info[8])])
    realtime_df = pd.DataFrame(realtime_list, columns=['code', 'date', 'open', 'high', 'low', 'close'])
    return realtime_df


if __name__ == '__main__':
    df = realtime(code='AU2206')
    print(df)
