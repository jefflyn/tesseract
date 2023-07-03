import datetime
import time

import pandas as pd
from akshare.futures.symbol_var import symbol_varieties

from zillion.future.domain import trade, basic, contract, nstat
from zillion.future.future_util import calc_position
from zillion.utils import notify_util, date_util
from zillion.utils.date_util import convert_to_date
from zillion.utils.price_util import future_price

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

init_target = {
    'SC2308': [[-450], [560]],
    'TA2309': [[-5200], [6000]],
    'EB2309': [[-7000], [8700]],
    'PG2309': [[-4000], [5000]],
    'NR2309': [[-9200], [10000]],
    'PP2309': [[-6800], [7400]],

    'RM2309': [[-2700], [3300]],
    'OI2309': [[-7400], [9350]],
    'P2309': [[-6300], [7800]],
    'PK2311': [[-9300], [10300, 10800]],
    'CJ2309': [[-9900], [10800]],
    'CF2309': [[-16600], [16800]],

    'SP2309': [[-5050], [5300]],
    'SF2309': [[-6800], [7500]],
    'SF2310': [[-6840], [6900]],
    'I2309': [[-660], [850]],
    'JM2309': [[-1200], [1600]],
    'J2309': [[-2000], [3000]],
    'UR2309': [[-1600], [1900]],
    'SA2309': [[-1550], [1749]],
    'FG2309': [[-1350], [1550]],

    # 'AG2308': [[-5500], [6000]],
    # 'SN2307': [[-200000], [228000]],
    # 'NI2309': [[-150000], [183000]],
    # 'AL2309': [[-17345.0], [20000]],
    # 'SI2308': [[-12000], [13530]],
}

holding_cost = {
    'TA2309': [-5946, 0], 'PP2309': [7293, 0], 'EB2309': [8000, 0], 'PG2309': [5000, 0],
    'FG2309': [1546, 0], 'SA2309': [1962, 4], 'SF2310': [6896, 2], 'I2309': [736, 0],
    'UR2309': [1928, 7], 'JM2309': [1300, 0], 'J2309': [2000, 0], 'SI2308': [12550, 600],
    'OI2309': [7900, 2000], 'P2309': [1974, 0], 'PK2311': [9984, 0], 'RM2309': [-10524, 0],
    'AL2308': [15000, 0], 'AG2308': [1234, 0], 'SN2308': [200000, 0], 'NI2308': [184000, 1],
    'SP2309': [5106, 0], 'CJ2309': [10080, 0], 'NR2309': [9000, 0], 'CF2309': [-16760, 0]
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


def format_percent(chg=None):
    return ('+' + str(chg) if chg > 0 else str(chg)) + '%'


if __name__ == '__main__':
    basic_df = basic.get_future_basics()
    contract_map = contract.contract_map
    nstat_map = nstat.nstat_map
    target_dw_index_dir = {}
    target_up_index_dir = {}
    high_dir = {}
    low_dir = {}
    today = date_util.today
    while True:
        realtime_df = None
        for code in init_target.keys():
            cont = contract_map.get(code)
            nst = nstat_map.get(code)
            if cont is None:
                print(code + ' is not in contract list!!!')
                continue
            his_low = cont.low
            his_low_date = cont.low_date
            low_diff = date_util.date_diff(convert_to_date(his_low_date), today)
            his_high = cont.high
            his_high_date = cont.high_date
            high_diff = date_util.date_diff(convert_to_date(his_high_date), today)
            his_low_date = his_low_date[2:]
            his_high_date = his_high_date[2:]
            realtime = trade.realtime_simple(code)
            price = realtime.iloc[0].at["close"]
            hist_pos = calc_position(price, his_low, his_high)
            pre_settle = realtime.iloc[0].at["pre_settle"]
            open = realtime.iloc[0].at["open"]
            high = realtime.iloc[0].at["high"]
            low = realtime.iloc[0].at["low"]
            bid = realtime.iloc[0].at["bid"]
            ask = realtime.iloc[0].at["ask"]
            hl_tag = '!' if low_diff < 8 or high_diff < 8 else ''
            hl_tag = '_' if low <= his_low else '^' if high >= his_high else hl_tag
            if low < his_low:
                contract.update_contract_hl(code, low, date_util.now_str())
                print("update hist low to contract")
            if high > his_high:
                contract.update_contract_hl(code, high, date_util.now_str())
                print("update hist high to contract")

            earning = ''
            if code in holding_cost.keys():
                symbol = symbol_varieties(code)
                step = basic_df.loc[symbol].at["step"]
                profit = basic_df.loc[symbol].at["profit"]
                cost_info = holding_cost.get(code)
                cost = cost_info[0]
                is_long = True if cost > 0 else False
                quantity = cost_info[1]
                cost_diff = (price - cost) if is_long else (abs(cost) - price)
                b2z = round(cost_diff * 100 / price, 2)
                # b2z = '-' + str(b2z) if cost_diff > 0 else str(abs(b2z))
                earning = future_price(cost_diff * (profit / step) * quantity) + ' ' + format_percent(b2z)
                earning = ('^' if is_long else '_') + future_price(cost_diff) + ',' + earning if quantity > 0 else ''

            if target_dw_index_dir.get(code) is None:
                target_dw_index_dir[code] = 0
                high_dir[code] = high
            if target_up_index_dir.get(code) is None:
                target_up_index_dir[code] = 0
                low_dir[code] = low

            avg60d = nstat.get_attr(nst, 'avg60d')
            pt60 = round((price - avg60d) * 100 / avg60d, 2)
            realtime['avg60d'] = '(' + str(avg60d) + ',' + format_percent(pt60) + ')'
            realtime['lo_hi'] = '[' + future_price(low) + '-' + future_price(high) + ' ' + future_price(
                high - low) + ']'
            # realtime['diff'] = future_price(high - low)
            price_diff = float(price) - float(pre_settle)
            realtime["change"] = format_percent(round(price_diff / float(pre_settle) * 100, 2)) \
                                 + ' ' + future_price(price_diff)
            open_flag = '↑' if open > pre_settle else ('↓' if open < pre_settle else ' ')
            realtime['open'] = '[' + future_price(pre_settle) + '-' + future_price(open) + ' ' \
                               + future_price(open - pre_settle) + ',' + format_percent(
                round((open - pre_settle) * 100 / pre_settle, 2)) + ']' + open_flag
            realtime['bid_ask'] = '(' + future_price(bid) + ',' + future_price(ask) + ')'
            position = 0
            if high != low:
                position = calc_position(price, low, high)
            elif high == low > price:
                position = 100
            if position == 0 and low_dir.get(code) > low:
                low_dir[code] = low
                notify_util.notify('📣' + code + ' @' + date_util.time_str(),
                                   '❄️❄️❄️' if low <= his_low else '🌧🌧🌧', '⬇️' + str(price))
            elif position == 100 and high_dir.get(code) < high:
                high_dir[code] = high
                notify_util.notify('📣' + code + ' @' + date_util.time_str(),
                                   '️🔥🔥🔥' if high >= his_high else '☀️☀️☀️', '⬆️' + str(price))

            realtime["pos"] = str(position) + '-' + str(hist_pos)
            realtime["code"] = hl_tag + code
            # realtime["his_hl"] = '^' + future_price(his_high) + '@' + his_high_date \
            #     if hist_pos > 50 else '_' + future_price(his_low) + '@' + his_low_date
            up_ = '[' + his_low_date + '-' + his_high_date + ',' + future_price(his_low) + '-' + future_price(
                his_high) + ']↑' + '(' + str(round((his_high - his_low) * 100 / his_low, 2)) + ',' \
                  + format_percent(round((price - his_high) * 100 / his_high, 2)) + ')'
            down_ = '[' + his_high_date + '-' + his_low_date + ',' + future_price(his_high) + '-' + future_price(
                his_low) + ']↓' + '(' + str(round((his_low - his_high) * 100 / his_high, 2)) + ',' \
                    + format_percent(round((price - his_low) * 100 / his_low, 2)) + ')'
            realtime["his_hl"] = up_ if his_low_date < his_high_date else down_

            target_list = init_target.get(code)
            target_diff = []
            target_dw_index = target_dw_index_dir.get(code)
            target_up_index = target_up_index_dir.get(code)
            realtime["target"] = str([target_list[0][target_dw_index], target_list[1][target_up_index]])
            for target_arr in target_list:
                is_target_down = target_arr[0] < 0
                price_str = str(price)
                if is_target_down:
                    target_price = target_arr[target_dw_index]
                    if price <= abs(target_price):
                        notify_util.notify('📣' + code + ' @' + date_util.time_str(),
                                           '🏁' + str(abs(target_price)), '🌚' + price_str)
                        new_target = round(target_price - target_price * 0.001)
                        if new_target not in init_target[code][0]:
                            init_target[code][0].append(new_target)
                        target_dw_index_dir[code] = target_dw_index + 1
                    elif target_dw_index > 0:
                        if price > abs(target_arr[target_dw_index - 1]):
                            target_dw_index_dir[code] = target_dw_index - 1
                else:
                    target_price = target_arr[target_up_index]
                    if target_price <= price:
                        notify_util.notify('📣' + code + ' @' + date_util.time_str(),
                                           '🏁' + str(target_price), '🌝️' + price_str)
                        new_target = round(target_price + target_price * 0.001)
                        if new_target not in init_target[code][1]:
                            init_target[code][1].append(new_target)
                        target_up_index_dir[code] = target_up_index + 1
                    elif target_up_index > 0:
                        if price < abs(target_arr[target_up_index - 1]):
                            target_up_index_dir[code] = target_up_index - 1
                diff = abs(target_price) - price
                target_diff.append(round(diff) if '.0' in str(diff) else round(diff, 1))
                realtime["t_diff"] = str(target_diff)
                realtime["earning"] = earning
            if realtime_df is None:
                realtime_df = realtime
            else:
                realtime_df = pd.concat([realtime_df, realtime], ignore_index=True)
        realtime_df = realtime_df.drop(columns=['pre_settle'])
        realtime_df = realtime_df.drop(columns=['low'])
        realtime_df = realtime_df.drop(columns=['high'])
        final_df = format_realtime(realtime_df)
        print(
            final_df[['code', 'open', 'change', 'lo_hi', 'close', 'bid_ask', 'pos', 'avg60d', 'his_hl',
                      'target', 't_diff', 'earning']])
        print(datetime.datetime.now())
        time.sleep(2)
