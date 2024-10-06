import time

import pandas as pd
from akshare.futures.symbol_var import symbol_varieties

from zillion.future import future_util, db_util
from zillion.future.app.live import format_percent
from zillion.future.domain import trade, basic, contract, nstat, daily
from zillion.future.future_util import calc_position
from zillion.utils import date_util
from zillion.utils.price_util import future_price

columns = ['code', 'pre_set', 'open', 'type', 'gap', 'gap_pr', 'fill',
           'change', 'limdw', 'limup', 'close', 'bid', 'ask', 'volume', 'hold',
           'a5d', 'a20d', 'a60d', 'a5d_ch', 'a20d_ch', 'a60d_ch',
           'cot_a', 'cot_b', 'trend', 'cota_ch', 'cotb_ch',
           'lo_hi', 'pos', 'lim_pos', 'c_lo_hi', 'c_pos', 'h_lo_hi', 'h_pos', 'update_time']


def realtime_monitor(df):
    print('')


def update_hl(code, low, high, c_low, c_high, h_low, h_high):
    if float(low) < float(c_low):
        contract.update_hl(code, low, date_util.now_str(), None, None)
    if float(high) > float(c_high):
        contract.update_hl(code, None, None, high, date_util.now_str())

    if float(low) < float(h_low):
        contract.update_hl(code, low, date_util.now_str(), None, None, True)
    if float(high) > float(h_high):
        contract.update_hl(code, None, None, high, date_util.now_str(), True)


def get_open_gap(code, open, pre_settle, low, high, pre_low, pre_high):
    gap = 0
    gap_price = 0
    is_fill = 0
    # open
    if open > pre_settle:
        open_type = '高开'
    elif open < pre_settle:
        open_type = '低开'
    else:
        open_type = '平开'
    # gap
    if open < pre_low:
        open_type = '_跳空低开'
        gap = round((open - pre_low) * 100 / pre_low, 2)
        gap_price = pre_low
        is_fill = -1
    elif open > pre_high:
        open_type = '_跳空高开'
        gap = round((open - pre_high) * 100 / pre_high, 2)
        gap_price = pre_high
        is_fill = -1
    if (open_type == '_跳空低开' and high >= pre_low) or (open_type == '_跳空高开' and low <= pre_high):
        is_fill = 1
        # print(code, "filled")
    return [pre_settle, open, open_type, gap, gap_price, is_fill]


if __name__ == '__main__':
    basic_df = basic.get_future_basics()
    contract_map = contract.contract_map
    contract_codes = list(contract_map.keys())
    last_daily = daily.get_pre_trading(contract_codes)
    nstat_map = nstat.nstat_map
    add_flag = False
    while True:
        codes = contract_codes
        now = date_util.now()
        if 21 <= now.hour <= 23:
            nigh_symbols = list(basic_df[basic_df.night == 1]['symbol'])
            codes = [c for c in codes if symbol_varieties(c) in nigh_symbols]
        realtime_df = trade.realtime(codes)
        # print(codes)
        # print(list(realtime_df['code']))
        result_data = []
        limit_up_info = []
        limit_dw_info = []
        up_high = []
        deep_down = []
        for index, realtime in realtime_df.iterrows():
            code = realtime['code']
            result_list = [code]
            symbol = symbol_varieties(code)
            pre_settle = realtime['pre_settle']
            open = realtime['open']
            high = realtime['high']
            low = realtime['low']
            bid = realtime['bid']
            ask = realtime['ask']
            price = realtime['close']
            # basic
            # basic = basic_df[basic_df.symbol == symbol]
            # daily
            last = last_daily[last_daily.code == code]
            if last is None or last.empty:
                continue
            else:
                pre_low = last.iloc[0].at['low']
                pre_high = last.iloc[0].at['high']
            # contract
            contra = contract_map.get(code)
            c_low = contra.low
            c_high = contra.high
            h_low = contra.h_low
            h_high = contra.h_high
            update_hl(code, low, high, c_low, c_high, h_low, h_high)
            # n stat
            nst = nstat_map.get(code)

            # part1 ['pre_settle', 'open', 'open_type', 'gap', 'gap_price', 'is_fill']
            part1 = get_open_gap(code, open, pre_settle, low, high, pre_low, pre_high)

            # part2 ['change', 'lim_down', 'lim_up', 'close', 'bid', 'ask', 'volume', 'hold']
            price_diff = price - pre_settle
            change = round(price_diff / float(pre_settle) * 100, 2)
            lim_down = round(pre_settle * (1 - contra.limit / 100))
            lim_up = round(pre_settle * (1 + contra.limit / 100))
            part2 = [change, lim_down, lim_up,
                     price, realtime['bid'], realtime['ask'], realtime['volume'], realtime['hold']]
            if change > 3:
                up_high.append(code + ' ' + format_percent(change) + ' @' + future_price(price))
            if change < -3:
                deep_down.append(code + ' ' + format_percent(change) + ' @' + future_price(price))
            if high == price:
                limit_up_info.append(code + ' @' + future_price(price) + ' ' + format_percent(change))
            elif price == low:
                limit_dw_info.append(code + ' @' + future_price(price) + ' ' + format_percent(change))

            # part3 ['a5d', 'a20d', 'a60d', 'a5d_ch', 'a20d_ch', 'a60d_ch']
            # change5d = nstat.get_attr(nst, '5d_change') if nst is not None else 0
            avg5d = price if nst is None else nstat.get_attr(nst, 'avg5d')
            avg20d = price if nst is None else nstat.get_attr(nst, 'avg20d')
            avg60d = price if nst is None else nstat.get_attr(nst, 'avg60d')
            part3 = [avg5d, avg20d, avg60d, round((price - avg5d) * 100 / avg5d, 2),
                     round((price - avg20d) * 100 / avg20d, 2),
                     round((price - avg60d) * 100 / avg60d, 2)]
            # part4 ['cot_a', 'cot_b', 'cot_trd', 'cota_ch', 'cotb_ch']
            c_low_date = contra.low_date
            c_high_date = contra.high_date
            cot_a = c_low if c_low_date < c_high_date else c_high
            cot_b = c_high if c_low_date < c_high_date else c_low
            cot_trd = 'up' if c_low_date < c_high_date else 'down'
            cota_ch = round((cot_b - cot_a) * 100 / cot_a, 2)
            cotb_ch = round((price - cot_b) * 100 / cot_b, 2)
            part4 = [cot_a, cot_b, cot_trd, cota_ch, cotb_ch]
            # part5 ['lo_hi', 'pos', 'lim_pos', 'c_lo_hi', 'c_pos', 'h_lo_hi', 'h_pos', 'update_time']
            pos = calc_position(price, low, high)
            c_pos = calc_position(price, c_low, c_high)
            h_pos = calc_position(price, h_low, h_high)
            part5 = [future_price(low) + '-' + future_price(high), pos, calc_position(price, lim_down, lim_up),
                     future_price(c_low) + '-' + future_price(c_high), c_pos,
                     future_price(h_low) + '-' + future_price(h_high), h_pos,
                     date_util.now()]
            result_list = result_list + part1 + part2 + part3 + part4 + part5
            result_data.append(result_list)
        result_df = pd.DataFrame(result_data, columns=columns)
        db_util.to_db(result_df, 'realtime', db_name='future')

        ## add index log begin
        time_str = str(now.hour) + ':' + str(now.minute)
        result_df['date'] = now.date()
        result_df['time'] = time_str
        df_mean = result_df.groupby(['date', 'time'])[['change']].mean()
        df_mean.insert(loc=0, column='date', value=now.date())
        df_mean.insert(loc=1, column='time', value=time_str)
        df_mean['change'] = df_mean['change'].apply(lambda x: round(x, 2))
        df_mean = df_mean.reset_index(drop=True)
        at_minutes = now.minute in [1, 11, 21, 31, 41, 51]
        if at_minutes is False:
            add_flag = False
        if future_util.is_trade_time() and add_flag is False and at_minutes:
            db_util.to_db(df_mean, 'realtime_index', if_exists='append', db_name='future')
            add_flag = True
        df_mean['change'] = df_mean['change'].apply(lambda x: format_percent(x))
        print(df_mean)
        ## add index log end
        print(now)
        print('UP', up_high)
        print(limit_up_info)
        print('DOWN', deep_down)
        print(limit_dw_info)
        if not future_util.is_trade_time():
            break
        time.sleep(2)
