import time

import pandas as pd

from zillion.future import future_util, db_util
from zillion.future.domain import trade, basic, contract, nstat
from zillion.future.future_util import calc_position
from zillion.utils import notify_util, date_util
from zillion.utils.date_util import convert_to_date
from zillion.utils.price_util import future_price

columns = ['code', 'open', 'change', 'close', 'low', 'high', 'volume', 'amount', 'famout', 'current',
           'wave',
                   'bottom', 'uspace',
                   'dspace', 'top', 'position', 'suggest']

def realtime_monitor(df):
    print("")




if __name__ == '__main__':
    basic_df = basic.get_future_basics()
    contract_map = contract.contract_map
    nstat_map = nstat.nstat_map
    high_dir = {}
    low_dir = {}
    today = date_util.today
    while True:
        realtime_df = trade.realtime(contract_map.keys())
        result_data = []
        for index, realtime in realtime_df.iterrows():
            code = realtime['code']
            pre_settle = realtime["pre_settle"]
            open = realtime["open"]
            high = realtime["high"]
            low = realtime["low"]
            bid = realtime["bid"]
            ask = realtime["ask"]
            price = realtime["close"]
            price_diff = price-pre_settle
            realtime["change"] = round(price_diff / float(pre_settle) * 100, 2)

            contra = contract_map.get(code)
            nst = nstat_map.get(code)
            c_low = contra.low
            c_low_date = contra.low_date
            low_diff = date_util.date_diff(c_low_date, today)
            c_high = contra.high
            c_high_date = contra.high_date
            high_diff = date_util.date_diff(convert_to_date(c_high_date), today)
            h_low = contra.h_low
            h_high = contra.h_high


            hist_pos = calc_position(price, c_low, c_high)


            # hl_tag = '!' if low_diff < 8 or high_diff < 8 else ''
            # hl_tag = '_' if low <= c_low else ('^' if high >= c_high else hl_tag)
            # if float(low) < float(c_low):
            #     contract.update_hl(code, low, date_util.now_str(), None, None)
            #     print(code, "update contract low!")
            # if float(low) < float(h_low):
            #     contract.update_hl(code, low, date_util.now_str(), None, None, True)
            #     print(code, "update hist low!")
            # if float(high) > float(c_high):
            #     contract.update_hl(code, None, None, high, date_util.now_str())
            #     print(code, "update contract high!")
            # if float(high) > float(h_high):
            #     contract.update_hl(code, None, None, high, date_util.now_str(), True)
            #     print(code, "update hist high!")

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

            if realtime_df is None:
                realtime_df = realtime
            else:
                realtime_df =
            result_data.append([])

        result_df = pd.DataFrame(result_data, columns=columns)
        db_util.to_db(result_df, 'realtime', db_name='future')
        # index end
        print(
            result_list[['code', 'open', 'change', 'lo_hi', 'close', 'bid_ask', 'pos', 'code', '5d_chg', 'avg_60_20', 'ct_hl',
                      'hist_hl', 'earning']])
        if not future_util.is_trade_time():
            break
        time.sleep(2)
