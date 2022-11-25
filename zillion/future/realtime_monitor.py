import datetime
import time

import pandas as pd

from zillion.future import future_trade
from zillion.utils import notify_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

code_target = {
    # 'PG2212': [-5000, 5200],
    'EB2301': [-7700, 7810],
    # 'PP2301': [-7522, 7800],
    'NR2301': [-9300, 9600],
    'UR2301': [-2610, 2635],
    # 'FG2301': [-1356, 1372],
    # 'SP2301': [-6600, 7000],
    #
    # 'NI2302': [-190000, 205000],
    # 'SN2301': [-151000, 166000],
    # 'AL2301': [-17345.0, 18800],
    # 'AG2301': [-4500, 4700],
    # 'JM2301': [-1900, 2100],
    # 'J2301': [-2450, 2650],
    'SF2301': [-8350, 8520],
    # 'I2301': [-710, 740],
    #
    # 'CJ2301': [-10625, 10880],
    # 'PK2301': [-10000, 11208],
    'P2301': [-8200, 8316],
    # 'OI2301': [-11100, 11900],
# 'OI2305': [-10000, 10600],
    # 'RM2301': [-2950, 3250],
    # 'CF2305': [-12080, 13110],
}


def format_realtime(df):
    '''
    格式化数据
    :param df:
    :return:
    '''
    # format data
    # df['open'] = df['open'].apply(lambda x: future_price(x))
    # df['low'] = df['low'].apply(lambda x: '_' + future_price(x))
    # df['high'] = df['high'].apply(lambda x: '^' + future_price(x))
    # df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['close'] = df['close'].apply(lambda x: '【' + future_price(x) + '】')
    df['bid'] = df['bid'].apply(lambda x: future_price(x))
    df['ask'] = df['ask'].apply(lambda x: future_price(x))
    # df['settle'] = df['settle'].apply(lambda x: future_price(x))
    return df


def future_price(price):
    price_str = str(price)
    price_arr = price_str.split(".")
    if len(price_arr) == 1:
        return price_arr[0]
    else:
        decimal = price_arr[1]
        if int(decimal) == 0:
            return price_arr[0]
        else:
            return price_arr[0] + '.' + decimal


if __name__ == '__main__':
    while True:
        realtime_df = None
        for code in code_target.keys():
            realtime = future_trade.realtime(code)
            price = realtime.iloc[0].at["close"]
            pre_settle = realtime.iloc[0].at["pre_settle"]
            open = realtime.iloc[0].at["open"]
            high = realtime.iloc[0].at["high"]
            low = realtime.iloc[0].at["low"]
            realtime['hi-low'] = '[' + future_price(low) + '-' + future_price(high) + ']'
            realtime['diff'] = future_price(high - low)
            price_diff = float(price) - float(pre_settle)
            realtime["change"] = str(round(price_diff / float(pre_settle) * 100, 2)) + "% " + future_price(price_diff)
            realtime['open'] = '[' + future_price(pre_settle) + '-' + future_price(open) \
                               + " " + future_price(open - pre_settle) + ']'

            position = 0
            if high != low:
                position = round((price - low) / (high - low) * 100, 2)
            elif high == low > price:
                position = 100
            realtime["position"] = round(position)
            target_list = code_target.get(code)
            target_diff = list()
            realtime["target"] = str(target_list)
            for target in target_list:
                price_str = str(price)
                if target < 0 and price <= abs(target):
                    notify_util.notify('📣' + code, '✔️' + str(abs(target)), '🌧' + price_str)
                    code_target[code][0] = round(target - target * 0.001) if '.0' in price_str else round(target - target * 0.001, 1)
                elif 0 < target <= price:
                    notify_util.notify('📣' + code, '✔️' + str(target), '☀️' + price_str)
                    code_target[code][1] = round(target + target * 0.001) if '.0' in price_str else round(target + target * 0.001, 1)
                target_diff.append(round(abs(target) - price))
                realtime["t_diff"] = str(target_diff)
            if realtime_df is None:
                realtime_df = realtime
            else:
                realtime_df = pd.concat([realtime_df, realtime], ignore_index=True)
        realtime_df = realtime_df.drop(columns=['pre_settle'])
        realtime_df = realtime_df.drop(columns=['low'])
        realtime_df = realtime_df.drop(columns=['high'])
        final_df = format_realtime(realtime_df)
        print(
            final_df[['code', 'date', 'open', 'hi-low', 'diff', 'close', 'bid', 'ask', 'change', 'position', 'target',
                      't_diff']])
        print(datetime.datetime.now())
        time.sleep(2)
