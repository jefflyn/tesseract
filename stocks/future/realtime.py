import sys
import time
from sys import argv

import pandas as pd
import requests

from stocks.future import future_const

KEYS = ['my', 'ec', 'pm', 'fm', 'nfm', 'ap', 'fp']
FOCUS = ['C2009', 'EG2005', 'CF2009']


def get_contract_keys(key_type=None):
    targets = ','.join(FOCUS)
    if type == 'ec':
        targets = ','.join(future_const.ENERGY_CHEMICAL.keys())
    elif type == 'pm':
        targets = ','.join(future_const.PRECIOUS_METAL.keys())
    elif type == 'fm':
        targets = ','.join(future_const.FERROUS_METAL.keys())
    elif type == 'nfm':
        targets = ','.join(future_const.NON_FERROUS_METAL.keys())
    elif type == 'ap':
        targets = ','.join(future_const.AGRICULTURAL_PRODUCTS.keys())
    elif type == 'fp':
        targets = ','.join(future_const.FINANCIAL.keys())

    return targets


def format_realtime(df):
    # format data
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    return df


def re_exe(type, interval=30, sortby=None):
    req_url = 'http://hq.sinajs.cn/list='
    while True:
        result = requests.get(req_url + get_contract_keys(type))
        txt = result.text
        # print(txt)
        if txt is not None and len(txt.split(';')) > 0:
            groups = txt.split(';\n')
            result_list = []
            for content in groups:
                if len(content) == 0:
                    continue
                info = content.split('=')[1].replace('"', '').strip().split(',')
                if len(info) < 18:
                    continue
                name = info[0]  # 0：名字
                # 1：不明数字
                open = float(info[2])  # 2：开盘价
                high = float(info[3])  # 3：最高价
                # 4：最低价
                low = float(info[4])
                # 5：昨日收盘价
                pre_close = float(info[5])
                # 6：买价，即“买一”报价
                bid = float(info[6])
                # 7：卖价，即“卖一”报价
                ask = float(info[7])
                # 8：最新价，即收盘价
                price = float(info[8])
                # 9：结算价
                settle = float(info[9])
                # 10：昨结算
                pre_settle = float(info[10])
                # 11：买量
                # 12：卖量
                # 13：持仓量
                # 14：成交量
                # 15：商品交易所简称
                exchange = info[15]
                # 16：品种名简称
                alias = info[16]
                # 17：日期
                trade_date = info[17]

                price_diff = float(price) - float(pre_settle)
                change = round(price_diff / float(pre_settle) * 100, 2)
                position = 0
                if high != low:
                    position = round((price - low) / (high - low) * 100, 2)
                elif high == low > price:
                    position = 100

                row_list = [name, exchange, price, change, bid, ask, low, high, position, trade_date]
                result_list.append(row_list)
            df = pd.DataFrame(result_list, columns=['contract', 'exchange', 'price', 'change',
                                                    'bid1', 'ask1', 'low', 'high', 'position', 'date'])
            if sortby == 'p':
                df = df.sort_values(['position'], ascending=False)
            else:
                df = df.sort_values(['change'])

            final_df = format_realtime(df)
            if final_df.empty:
                print('no data, exit!')
                break
            print(final_df)
            time.sleep(interval)


if __name__ == '__main__':
    """
    python realtime.py argv1 argv2[c|p]
    nohup /usr/local/bin/redis-server /usr/local/etc/redis.conf &
    nohup /usr/local/bin/redis-server /etc/redis.conf &
    """
    if len(argv) > 1:
        type = argv[1]
        if type not in KEYS:
            print("Contract Type NOT defined. Try the followings: " + str(KEYS))
            sys.exit(0)
    else:
        type = 'my'
    if len(argv) > 2 and argv[2] in ['c', 'p']:
        sort = argv[2]
    else:
        sort = 'c'

    re_exe(type, 30, sortby=sort)
