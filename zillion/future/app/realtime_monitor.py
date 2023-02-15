import datetime
import time

import pandas as pd

from zillion.future.domain import trade
from zillion.utils import notify_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

init_target = {
    'SC2304': [[-555], [572]],
    'TA2305': [[-5420], [5500]],
    # 'PG2304': [-4250, 4650],
    # 'EB2304': [-8320, 8880],
    # 'PP2305': [-7670, 8000],
    # 'NR2305': [-9750, 10000],
    # 'UR2305': [-2490, 2635],
    # 'FG2305': [-1356, 1372],
    # 'SP2305': [-6700, 6930],
    #
    # 'NI2304': [-197000, 208000],
    # 'SN2304': [-218500, 241000],
    # 'AL2304': [-17345.0, 19800],
    'SI2308': [[-17580], [18260]],
    # 'AG2305': [-4500, 5000],
    # 'JM2305': [-1900, 2100],
    # 'J2305': [-2450, 2650],
    'SF2305': [[-7700], [7970]],
    'I2305': [[-800], [900]],
    #
    # 'CJ2305': [-10060, 10460],
    # 'PK2304': [-10000, 10600],
    # 'P2305': [-7600, 8400],
    'OI2305': [[-9740], [9850]],
    # 'RM2305': [-2950, [3250]],
    # 'CF2305': [-14080, 14500]],
    'AP2305': [[-8780], [8880]],
    'FG2305': [[-1500], [1650]],
    'SA2309': [[-2470], [2490]],
        'PP2305': [[-7780], [7810]],
'EB2304': [[-8310], [8320]],
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
    price_str = str(round(price, 2))
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
    target_dw_index_dir = {}
    target_up_index_dir = {}
    while True:
        realtime_df = None
        for code in init_target.keys():
            if target_dw_index_dir.get(code) is None:
                target_dw_index_dir[code] = 0
            if target_up_index_dir.get(code) is None:
                target_up_index_dir[code] = 0
            realtime = trade.realtime_simple(code)
            price = realtime.iloc[0].at["close"]
            pre_settle = realtime.iloc[0].at["pre_settle"]
            open = realtime.iloc[0].at["open"]
            high = realtime.iloc[0].at["high"]
            low = realtime.iloc[0].at["low"]
            realtime['low-hi'] = '[' + future_price(low) + '-' + future_price(high) + ']'
            realtime['diff'] = future_price(high - low)
            price_diff = float(price) - float(pre_settle)
            realtime["change"] = str(round(price_diff / float(pre_settle) * 100, 2)) + "% " + future_price(price_diff)
            is_up = open > pre_settle
            realtime['open'] = '[' + future_price(pre_settle) + '-' + future_price(open) + (' ↑' if is_up else ' ↓') \
                               + future_price(open - pre_settle) + ']'

            position = 0
            if high != low:
                position = round((price - low) / (high - low) * 100, 2)
            elif high == low > price:
                position = 100
            realtime["position"] = round(position)
            target_list = init_target.get(code)
            target_diff = list()
            target_dw_index = target_dw_index_dir.get(code)
            target_up_index = target_up_index_dir.get(code)
            realtime["target"] = str([target_list[0][target_dw_index], target_list[1][target_up_index]])
            for target_arr in target_list:
                is_target_down = target_arr[0] < 0
                price_str = str(price)
                if is_target_down:
                    target_price = target_arr[target_dw_index]
                    if price <= abs(target_price):
                        notify_util.notify('📣' + code, '✔️' + str(abs(target_price)), '🌧' + price_str)
                        new_target = round(target_price - target_price * 0.001) if '.0' in price_str else round(
                            target_price - target_price * 0.001, 1)
                        init_target[code][0].append(new_target)
                        target_dw_index_dir[code] = target_dw_index + 1
                    elif target_dw_index > 1:
                        if price > abs(target_arr[target_dw_index - 1]):
                            target_dw_index_dir[code] = target_dw_index - 1
                else:
                    target_price = target_arr[target_up_index]
                    if target_price <= price:
                        notify_util.notify('📣' + code, '✔️' + str(target_price), '☀️' + price_str)
                        new_target = round(target_price + target_price * 0.001) if '.0' in price_str else round(
                            target_price + target_price * 0.001, 1)
                        init_target[code][1].append(new_target)
                        target_up_index_dir[code] = target_up_index + 1
                    elif target_up_index > 1:
                        if price < abs(target_arr[target_up_index - 1]):
                            target_up_index_dir[code] = target_up_index - 1
                target_diff.append(round(abs(target_price) - price))
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
            final_df[['code', 'date', 'open', 'low-hi', 'diff', 'close', 'bid', 'ask', 'change', 'position', 'target',
                      't_diff']])
        print(datetime.datetime.now())
        time.sleep(2)
