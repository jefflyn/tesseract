from datetime import datetime

import numpy as np
import pandas as pd

import stocks.util.db_util as _dt
from stocks.future import future_util, future_trade
from stocks.util import date_util


def add_realtime_data(code=None, local_last_trade_date=None):
    last_trade_date = date_util.get_today(date_util.FORMAT_FLAT)  # .get_latest_trade_date(1)[0]
    if local_last_trade_date < last_trade_date:  # not the latest record
        realtime = future_trade.realtime(code.split('.')[0])
        if realtime is not None and realtime.empty is False:
            realtime['code'] = code
            return realtime
    return None


def get_wave(code=None, hist_data=None, begin_low=True, duration=0, change=0):
    local_last_trade_date = list(hist_data['date'])[-1]
    realtime = add_realtime_data(code, local_last_trade_date)
    if realtime is not None:
        # hist_data = hist_data.append(realtime, ignore_index=True)
        hist_data = pd.concat([hist_data, realtime], ignore_index=True)
    new_code = code.split('.')[0]
    left_data = wave_from(new_code, hist_data, begin_low, 'left', duration, change)
    # sorted by date asc
    left_data.reverse()
    right_data = wave_from(new_code, hist_data, begin_low, 'right', duration, change)
    period_df = pd.DataFrame(left_data + right_data,
                             columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'change'])
    period_list = [period_df]
    if period_list is None or len(period_list) == 0:
        print('result is empty, please check the code is exist!')
        return None
    result = pd.concat(period_list, ignore_index=True)
    return result


def wave_from(code, df, begin_low, direction='left', duration=0, change=0):
    period_data = []
    first_date = df.head(1).at[df.head(1).index.to_numpy()[0], 'date']
    last_date = df.tail(1).at[df.tail(1).index.to_numpy()[0], 'date']

    # start from the lowest price, find the wave from both sides
    pivot_low = df.min()['close'] if df.min()['low'] == 0 else df.min()['low']
    pivot_rec = df[df.low == pivot_low]
    if pivot_rec is None or pivot_rec.empty is True:
        print(code + ' pivot_rec is None or pivot_rec.empty')
        return
    pivot_index = pivot_rec.index.to_numpy()[0]
    pivot_date = pivot_rec.at[pivot_index, 'date']
    pivot_close = pivot_rec.at[pivot_index, 'close']

    is_max = begin_low
    begin_date = first_date
    end_date = pivot_date
    begin_price = pivot_low
    end_price = pivot_low

    if direction == 'right':
        begin_date = pivot_date
        end_date = last_date
    diff_days = datetime.strptime(end_date, '%Y%m%d') - datetime.strptime(begin_date, '%Y%m%d')

    while diff_days.days > duration:
        data = df[(df.date >= begin_date) & (df.date < end_date)] if direction == 'left' else df[
            (df.date > begin_date) & (df.date <= end_date)]
        price = data.max()['high'] if is_max else data.min()['low']

        status = ''
        rec = data[data.high == price] if is_max else data[data.low == price]
        idx = rec.index.to_numpy()[0]
        date = rec.at[idx, 'date']
        close = rec.at[idx, 'close']

        if direction == 'left':
            begin_price = price
            begin_date = date
            status = 'down' if is_max else 'up'
        if direction == 'right':
            # if the latest one, get the close price, calculate the actual rises
            # end_price = close if date == last_date else price
            end_price = price
            end_date = date
            status = 'up' if is_max else 'down'

        diff_percent = 0
        if begin_price > 0:
            diff_percent = (end_price - begin_price) / begin_price * 100
        if abs(diff_percent) < change:
            break
        list = []
        # ['code', 'begin', 'end', 'status' 'begin_price', 'end_price', 'days', 'p_change']
        list.append(code)
        list.append(begin_date)
        list.append(end_date)
        list.append(status)
        list.append(begin_price)
        list.append(end_price)
        list.append((datetime.strptime(end_date, '%Y%m%d') - datetime.strptime(begin_date, '%Y%m%d')).days)
        list.append(round(diff_percent, 2))
        if begin_price != end_price:
            period_data.append(list)

        if direction == 'left':
            begin_date = first_date
            end_date = date
            end_price = price
        if direction == 'right':
            begin_date = date
            end_date = last_date
            begin_price = price

        diff_days = datetime.strptime(end_date, '%Y%m%d') - datetime.strptime(begin_date, '%Y%m%d')
        is_max = not is_max
    return period_data


def wave_to_str(wave_df=None, size=4, change=10):
    """
    :param wave_df:
    :param size:
    :param change:
    :return: 1.4,-1.9,2.12|10,20,13|15.4,10.9,20.12
    """
    if wave_df is None or size < 1:
        return ''
    changelist = list(wave_df['change'])
    less_than_change = max([abs(e) for e in changelist]) < change

    if len(changelist) <= size:
        wave_change_str = ','.join(list(map(str, changelist)))
        wave_day_str = ','.join(list(map(str, wave_df['days'])))
        wave_price_str = ','.join(list(map(str, wave_df['end_price'])))
    else:
        change_list = []
        sum_last = 0
        day_list = []
        sum_days = 0
        price_list = []
        sum_price = 0
        for index, row in wave_df.iterrows():
            last_one = row['change']
            wave_day = row['days']
            wave_end_price = row['end_price']
            # flag = row['status']
            if abs(last_one) >= change:
                if sum_last != 0:
                    change_list.append(round(sum_last, 2))
                    sum_last = 0
                    day_list.append(sum_days)
                    sum_days = 0
                    price_list.append(sum_price)
                    sum_price = 0
                price_list.append(round(wave_end_price, 2))
                change_list.append(round(last_one, 2))
                day_list.append(wave_day)
                continue
            else:
                sum_last += last_one
                sum_days += wave_day
                sum_price = sum_price if sum_price > 0 else round(wave_end_price, 2)
                if abs(sum_last) >= change:
                    change_list.append(round(sum_last, 2))
                    sum_last = 0
                    day_list.append(sum_days)
                    sum_days = 0
                    price_list.append(sum_price)
                    sum_price = 0
                    continue
                else:
                    # 最后一条记录
                    if index == len(changelist) - 1:
                        change_list.append(round(sum_last, 2))
                        day_list.append(sum_days)
                        price_list.append(sum_price)

        # 剔除多余的元素数量
        takes = len(change_list) - size if len(change_list) - size > 0 else 0
        change_list = change_list[takes:]
        day_list = day_list[takes:]
        takes_price = len(price_list) - size if len(price_list) - size > 0 else 0
        price_list = price_list[takes_price:]
        wave_change_str = ','.join(map(str, change_list))
        wave_day_str = ','.join(map(str, day_list))
        wave_price_str = ','.join(map(str, price_list))
    if wave_change_str == '' or less_than_change is True:
        length = len(changelist)
        wave_change_str = ','.join(list(map(str, changelist))[length - size:])
        wave_day_str = ','.join(list(map(str, wave_df['days']))[length - size:])
        wave_price_str = ','.join(list(map(str, wave_df['end_price']))[length - size:])
    return wave_change_str + '|' + wave_day_str + '|' + wave_price_str




def get_wave_ab(wave_str=None, pct_limit=33):
    if wave_str is None:
        return
    wavestr_ab = wave_str.split('\n')[0].split('|')
    wavestr_ab_list = list(reversed(wavestr_ab))
    wavestr_ab_list = [float(i) for i in wavestr_ab_list[0:len(wavestr_ab_list) - 1]]
    wave_day_ab = wave_str.split('\n')[1].split('|')
    wave_day_ab_list = list(reversed(wave_day_ab))
    wave_day_ab_list = [int(i) for i in wave_day_ab_list[0:len(wave_day_ab_list) - 1]]

    a_index = -1
    for idx, pct in enumerate(wavestr_ab_list):
        if pct == '':
            continue
        if idx == 0 and abs(float(pct)) >= pct_limit:
            a_index = idx
            break
        else:
            if abs(float(pct)) >= pct_limit:
                a_index = idx
                break

    if a_index == 0:
        wave_a = float(wavestr_ab_list[a_index]) if len(wavestr_ab_list) == 1 else float(wavestr_ab_list[a_index + 1])
        wave_b = 0 if len(wavestr_ab_list) == 1 else float(wavestr_ab_list[a_index])
        day_a = int(wave_day_ab_list[a_index]) if len(wave_day_ab_list) == 1 else int(wave_day_ab_list[a_index + 1])
        day_b = 0 if len(wave_day_ab_list) == 1 else int(wave_day_ab_list[a_index])
    elif a_index == -1:
        wave_a = float(wavestr_ab_list[0]) if len(wavestr_ab_list) == 1 else float(wavestr_ab_list[1])
        wave_b = 0 if len(wavestr_ab_list) == 1 else float(wavestr_ab_list[0])
        day_a = int(wave_day_ab_list[0]) if len(wave_day_ab_list) == 1 else int(wave_day_ab_list[1])
        day_b = 0 if len(wave_day_ab_list) == 1 else int(wave_day_ab_list[0])
    else:
        wave_a = float(wavestr_ab_list[a_index])
        wave_b = np.sum(wavestr_ab_list[0:a_index])
        day_a = int(wave_day_ab_list[a_index])
        day_b = np.sum(wave_day_ab_list[0:a_index])
    return [(wave_a, day_a), (wave_b, day_b)]


def get_wave_ab_fast(wave_str, pct_limit=33):
    wavestr_ab = wave_str.split('\n')[0].split('|')
    wavestr_ab_list = list(wavestr_ab)
    wavestr_ab_list = [float(i) for i in wavestr_ab_list[1:len(wavestr_ab_list)]]
    wave_day_ab = wave_str.split('\n')[1].split('|')
    wave_day_ab_list = list(wave_day_ab)
    wave_day_ab_list = [int(i) for i in wave_day_ab_list[1:len(wave_day_ab_list)]]

    max_incr = max(wavestr_ab_list)
    min_decr = min(wavestr_ab_list)
    is_fit = min_decr > -33 and max_incr < 50

    a_pct = 0.0
    a_day = 0
    b_pct = 0.0
    b_day = 0
    if len(wavestr_ab_list) == 1:
        a_pct = wavestr_ab_list.pop()
        a_day = wave_day_ab_list.pop()
    elif len(wavestr_ab_list) == 2:
        a_pct = wavestr_ab_list[0]
        b_pct = wavestr_ab_list[1]
        a_day = wave_day_ab_list[0]
        b_day = wave_day_ab_list[1]
    else:
        while len(wavestr_ab_list) > 0:
            pct = wavestr_ab_list.pop()
            day = wave_day_ab_list.pop()
            if (pct < 0 and abs(pct) >= pct_limit) or \
                    (pct < 0 and is_fit and abs(pct) >= 20) or \
                    (pct > 0 and is_fit and pct >= pct_limit) or \
                    (pct > 0 and pct >= 50):
                if b_pct == 0:
                    b_pct = pct
                    b_day = day
                else:
                    if abs(b_pct + pct) == abs(b_pct) + abs(pct):
                        b_pct += pct
                        b_day += day
                    else:
                        a_pct = pct
                        a_day = day
                break
            else:
                b_pct += pct
                b_day += day
        if len(wavestr_ab_list) > 0 and a_pct == 0:
            a_pct = wavestr_ab_list.pop()
            a_day = wave_day_ab_list.pop()
    # print(a_pct, b_pct)
    # print(a_day, b_day)
    return [(a_pct, a_day), (b_pct, b_day)]


def get_wave_list(wave_str=None, size=4):
    change_arr = wave_str.split('|')[0][0:].split(',')
    price_arr = wave_str.split('|')[2][0:].split(',')
    while len(change_arr) < size:
        change_arr.append(0)
    while len(price_arr) < size:
        price_arr.append(0)
    return [round(float(e), 2) for e in change_arr] + [round(float(e), 2) for e in price_arr]


def wave_to_db(wave_list=None, wave_detail_list=None):
    wave_df_result = pd.DataFrame(wave_list,
                                  columns=['code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp', 'dp'])
    _dt.to_db(wave_df_result, 'future_wave')
    wave_detail_result = pd.DataFrame(pd.concat(wave_detail_list),
                                      columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price',
                                               'change', 'days'])
    _dt.to_db(wave_detail_result, 'future_wave_detail')


if __name__ == '__main__':
    ############################################################
    select_ts_codes = "select ts_code from ts_future_contract where type in (1, 2) and fut_code " \
                      "in (select symbol from future_basic where deleted=0)"
    select_main_codes = "select concat(code, '.', exchange) ts_code from future_basic where deleted=0"
    ts_codes_df = future_util.select_from_sql(select_ts_codes)
    main_codes_df = future_util.select_from_sql(select_main_codes)
    code_list = list(pd.concat([ts_codes_df, main_codes_df])['ts_code'])
    ############################################################
    # code_list = ['APL.ZCE']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    for code in code_list:
        df_data = future_util.get_ts_future_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        # df_data['code'] = df_data['code'].apply(lambda x: str(x).split('.')[0])
        wave_df = get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)
        wave_detail_list.append(wave_df)
        wave_str = wave_to_str(wave_df)
        wave_list = get_wave_list(wave_str)
        wave_list.insert(0, code.split('.')[0])
        wave_list.insert(1, list(wave_df['begin'])[0])
        wave_list.insert(2, list(wave_df['end'])[-1])
        wave_data_list.append(wave_list)
        # print(result)
        # print(wave_str)
        # wave_ab = get_wave_ab(wave_str, 33)
        # print(wave_ab)
        # print('get_wave_ab_fast', get_wave_ab_fast(wave_str))

    wave_to_db(wave_data_list, wave_detail_list)
    print(date_util.get_now())
