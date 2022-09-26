import time

import pandas as pd

from zillion.future import future_trade
from zillion.utils import notify_util


def format_realtime(df):
    '''
    格式化数据
    :param df:
    :return:
    '''
    # format data
    df['open'] = df['open'].apply(lambda x: future_price(x))
    df['low'] = df['low'].apply(lambda x: future_price(x))
    df['high'] = df['high'].apply(lambda x: future_price(x))
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['close'] = df['close'].apply(lambda x: '【' + future_price(x) + '】')
    df['bid'] = df['bid'].apply(lambda x: future_price(x))
    df['ask'] = df['ask'].apply(lambda x: future_price(x))
    df['pre_settle'] = df['pre_settle'].apply(lambda x: future_price(x))
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
    code_target = {
        'PK2301': [-10854, 11100],
        'CF2301': [-13480, 13580],
                   }
    while True:
        realtime_df = None
        for code in code_target.keys():
            realtime = future_trade.realtime(code)
            price = realtime.iloc[0].at["close"]
            pre_settle = realtime.iloc[0].at["pre_settle"]
            high = realtime.iloc[0].at["high"]
            low = realtime.iloc[0].at["low"]
            price_diff = float(price) - float(pre_settle)
            realtime["change"] = round(price_diff / float(pre_settle) * 100, 2)

            position = 0
            if high != low:
                position = round((price - low) / (high - low) * 100, 2)
            elif high == low > price:
                position = 100
            realtime["position"] = position

            target_list = code_target.get(code)
            for target in target_list:
                if target < 0 and price < abs(target):
                    notify_util.notify(code, str(abs(target)), '↓' + str(price))
                    code_target[code][0] = target - target*0.02
                elif 0 < target < price:
                    notify_util.notify(code, str(target), '↑' + str(price))
                    code_target[code][1] = target + target*0.02
            if realtime_df is None:
                realtime_df = realtime
            else:
                realtime_df = pd.concat([realtime_df, realtime], ignore_index=True)
        final_df = format_realtime(realtime_df)
        print(final_df)
        time.sleep(2)
