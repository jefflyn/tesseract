import datetime
import statistics
import time

import pandas as pd
from akshare.futures.symbol_var import symbol_varieties

from zillion.future import future_util
from zillion.future.domain import trade, basic, contract, nstat
from zillion.future.future_util import calc_position
from zillion.utils import notify_util, date_util
from zillion.utils.date_util import convert_to_date
from zillion.utils.price_util import future_price
from zillion.utils.redis_util import redis_client


def realtime_monitor(df):



if __name__ == '__main__':
    basic_df = basic.get_future_basics()
    contract_map = contract.contract_map
    nstat_map = nstat.nstat_map
    target_dw_index_dir = {}
    target_up_index_dir = {}
    high_dir = {}
    low_dir = {}
    today = date_util.today
    hour_minute_map = {}
    while True:
        realtime_df = None
        for code in init_target.keys():
            contra = contract_map.get(code)
            nst = nstat_map.get(code)
            if contra is None:
                print(code + ' is not in contract list!!!')
                continue
            c_low = contra.low
            c_low_date = contra.low_date
            low_diff = date_util.date_diff(c_low_date, today)
            c_high = contra.high
            c_high_date = contra.high_date
            high_diff = date_util.date_diff(convert_to_date(c_high_date), today)
            h_low = contra.h_low
            h_high = contra.h_high

            realtime = trade.realtime_simple(code)
            price = realtime.iloc[0].at["close"]
            hist_pos = calc_position(price, c_low, c_high)
            pre_settle = realtime.iloc[0].at["pre_settle"]
            open = realtime.iloc[0].at["open"]
            high = realtime.iloc[0].at["high"]
            low = realtime.iloc[0].at["low"]
            bid = realtime.iloc[0].at["bid"]
            ask = realtime.iloc[0].at["ask"]
            hl_tag = '!' if low_diff < 8 or high_diff < 8 else ''
            hl_tag = '_' if low <= c_low else ('^' if high >= c_high else hl_tag)
            if float(low) < float(c_low):
                contract.update_hl(code, low, date_util.now_str(), None, None)
                print(code, "update contract low!")
            if float(low) < float(h_low):
                contract.update_hl(code, low, date_util.now_str(), None, None, True)
                print(code, "update hist low!")
            if float(high) > float(c_high):
                contract.update_hl(code, None, None, high, date_util.now_str())
                print(code, "update contract high!")
            if float(high) > float(h_high):
                contract.update_hl(code, None, None, high, date_util.now_str(), True)
                print(code, "update hist high!")

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
            change5d = nstat.get_attr(nst, '5d_change') if nst is not None else 0
            avg5d = price if nst is None else nstat.get_attr(nst, 'avg5d')
            avg20d = price if nst is None else nstat.get_attr(nst, 'avg20d')
            avg60d = price if nst is None else nstat.get_attr(nst, 'avg60d')
            avg5d_flag = '↑' if price >= avg5d else '↓'
            realtime['close'] = '【' + future_price(price) + '】' + avg5d_flag
            trend_flag = '🌗' if price >= avg20d else '🌑'

            pt60 = round((price - avg60d) * 100 / avg60d, 2)
            realtime['avg_60_20'] = '(' + str(avg60d) + ',' + format_percent(pt60) + ',' + str(avg20d) + ')' + trend_flag
            realtime['5d_chg'] = str(change5d) + '%'
            realtime['lo_hi'] = '[' + future_price(low) + '-' + future_price(high) + ' ' + future_price(
                high - low) + ']'
            # realtime['diff'] = future_price(high - low)
            price_diff = float(price) - float(pre_settle)
            realtime["change"] = round(price_diff / float(pre_settle) * 100, 2)
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
                                   '❄️❄️❄️' if low <= c_low else '🌧🌧🌧', '⬇️' + str(price))
            elif position == 100 and high_dir.get(code) < high:
                high_dir[code] = high
                notify_util.notify('📣' + code + ' @' + date_util.time_str(),
                                   '️🔥🔥🔥' if high >= c_high else '☀️☀️☀️', '⬆️' + str(price))
            # str(position) + '-' + str(hist_pos)
            realtime["pos"] = position
            realtime["pos_hist"] = hist_pos
            realtime["code"] = hl_tag + code
            # realtime["his_hl"] = '^' + future_price(his_high) + '@' + his_high_date \
            #     if hist_pos > 50 else '_' + future_price(his_low) + '@' + his_low_date
            up_ = '[' + future_price(c_low) + '-' + future_price(c_high) + ']↑' + '(' + format_percent(round((c_high - c_low) * 100 / c_low, 1)) + ',' \
                  + format_percent(round((price - c_high) * 100 / c_high, 1)) + ')'
            down_ = '[' + future_price(c_high) + '-' + future_price(c_low) + ']↓' + '(' + format_percent(round((c_low - c_high) * 100 / c_high, 1)) + ',' \
                    + format_percent(round((price - c_low) * 100 / c_low, 2)) + ')'
            realtime["ct_hl"] = up_ if c_low_date < c_high_date else down_
            hist_pos = calc_position(price, h_low, h_high)
            if hist_pos > 80 or hist_pos < 20:
                hist_pos = str(hist_pos) + '🌞' if hist_pos > 80 else str(hist_pos) + '❄️'
            realtime["hist_hl"] = ('[' + future_price(h_low) + '-' + future_price(h_high) + ' ' + str(hist_pos) + ']')
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
                                           '🏁' + str(abs(target_price)), '📉' + price_str)
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
                                           '🏁' + str(target_price), '📈' + price_str)
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
        # change pos
        realtime_df = realtime_df.sort_values(by=['pos'], ascending=False, ignore_index=True)
        # index ##
        now_time = datetime.datetime.now()
        hour_minute = str(now_time.hour) + '' + str(now_time.minute)
        key = 'index-' + date_util.curt_date
        if hour_minute not in hour_minute_map.keys() and now_time.minute in [1, 11, 21, 31, 41, 51]\
                and future_util.is_trade_time():
            avg_ch = str(round(statistics.mean(list(realtime_df['change'])), 2)) + ''
            redis_client.lpush(key, hour_minute + ': ' + avg_ch)
            hour_minute_map[hour_minute] = avg_ch
        # index end
        final_df = format_realtime(realtime_df)
        print(
            final_df[['code', 'open', 'change', 'lo_hi', 'close', 'bid_ask', 'pos', 'code', '5d_chg', 'avg_60_20', 'ct_hl',
                      'hist_hl', 'earning']])
        ###   'target', 't_diff', 'earning']])
        print(now_time, str(redis_client.lrange(key, 0, -1)))
        if not future_util.is_trade_time():
            break
        time.sleep(2)
