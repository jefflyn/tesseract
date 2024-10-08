# coding: utf-8
import time
from sys import argv

import pandas as pd
import tushare as ts

import zillion.utils.sms_util as sms
from zillion.stock.gene import wave
from zillion.utils import date_util, _utils, date_const
from zillion.utils.redis_util import redis_client

INDEX_SH = ['000001', '000016', '000300']
INDEX_SZ = ['399001', '399005']
INDEX_CYB = ['399006']

target = ['000001', '000016', '399001', '399005', '399006']


def format_index(df):
    """
    格式化数据
    :param df:
    :return:
    """
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['close'] = df['close'].apply(lambda x: str(round(x, 2)))
    df['low'] = df['low'].apply(lambda x: '_' + str(round(x, 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(x, 2)))
    df['bottom'] = df['bottom'].apply(lambda x: '[' + str(x))
    df['top'] = df['top'].apply(lambda x: str(x) + ']')
    df['uspace'] = df['uspace'].apply(lambda x: '+' + str(round(x, 2)) + '%')
    df['dspace'] = df['dspace'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    df['current'] = df['current'].apply(lambda x: str(round(x, 2)) + '%')
    return df


def get_status():
    index_df = ts.get_index()
    index_df = index_df[index_df['code'].isin(target)]
    morning_time = date_util.mid_close_time
    if date_util.open_time > date_util.now():
        morning_time = date_util.open_time
    if date_util.open_time < date_util.now() < date_util.mid_close_time:
        morning_time = date_util.now()

    afternoon_time = date_util.close_time
    if date_util.mid_open_time > date_util.now():
        afternoon_time = date_util.mid_open_time
    if date_util.mid_open_time < date_util.now() < date_util.close_time:
        afternoon_time = date_util.now()

    morning_seconds = round((morning_time - date_util.open_time).seconds / 60)
    afternoon_seconds = round((afternoon_time - date_util.mid_open_time).seconds / 60)

    result_data = []
    for index, row in index_df.iterrows():
        row_data = []
        code = row['code']
        row_data.append(code)
        row_data.append(row['name'])
        row_data.append(row['change'])
        current_point = row['close']
        row_data.append(current_point)
        low = row['low']
        high = row['high']
        row_data.append(low)
        row_data.append(high)
        row_data.append(row['volume'])
        trade_amount = row['amount']
        row_data.append(trade_amount)
        pre_amount = round(trade_amount / (morning_seconds + afternoon_seconds) * 60 * 4, 4)
        row_data.append(pre_amount)

        # get wave data and bottom top
        wavedf = wave.get_wave(code, is_index=True)
        wavestr = wave.wave_to_str(wavedf, size=3)
        bottomdf = wave.get_bottom(wavedf, limit=8)
        bottom = bottomdf.at[0, 'bottom']
        top = bottomdf.at[0, 'top']
        current = 0
        if high > low:
            current = (current_point - low) / (high - low) * 100
        position = (current_point - bottom) / (top - bottom) * 100
        uspace = (current_point - bottom) / bottom * 100
        dspace = (current_point - top) / top * 100
        row_data.append(current)
        row_data.append(wavestr)
        row_data.append(bottom)
        row_data.append(round(uspace, 2))
        row_data.append(round(dspace, 2))
        row_data.append(top)
        row_data.append(round(position, 2))

        suggest = suggest_by_position(code, position)
        row_data.append(suggest)
        result_data.append(row_data)

        # 在(-11, -2]范围告警:价格、涨跌幅等
        pct_chage = float(row['change']) if row['change'] is not None else 0
        if pct_chage > -11 and (pct_chage <= -2 or pct_chage < -3 or pct_chage < -4):
            key = date_util.get_today() + '_index_' + code + '_' + str(int(pct_chage))
            name_format = '：' + code + ' ' + row['name']
            price_format = str(round(float(row['change']), 2)) + '%'
            warn_times = redis_client.get(key)
            if warn_times is None:
                sms.send_msg_with_tencent(code, name_format, price_format)
                redis_client.set(key, row['name'] + price_format, ex=date_const.ONE_MONTH * 3)

    columns = ['code', 'name', 'change', 'close', 'low', 'high', 'volume', 'amount', 'famout', 'current', 'wave', 'bottom', 'uspace',
               'dspace', 'top', 'position', 'suggest']
    result_df = pd.DataFrame(result_data, columns=columns)
    result_df = result_df.sort_values('change')

    return result_df


def suggest_by_position(code, position):
    '''
    各市场水位建议
    :param code:
    :param position:
    :return:
    '''
    if code in INDEX_SH:
        if _utils.in_range(position, 0, 11):
            return 'suck'
        elif _utils.in_range(position, 11, 30):
            return 'buy'
        elif _utils.in_range(position, 30, 40):
            return 'hold'
        elif _utils.in_range(position, 40, 55):
            return 'sell'
        elif _utils.in_range(position, 55):
            return 'out'
    elif code in INDEX_SZ:
        if _utils.in_range(position, 0, 20):
            return 'suck'
        elif _utils.in_range(position, 20, 35):
            return 'buy'
        elif _utils.in_range(position, 35, 60):
            return 'hold'
        elif _utils.in_range(position, 60, 75):
            return 'sell'
        elif _utils.in_range(position, 75):
            return 'out'
    elif code in INDEX_CYB:
        if _utils.in_range(position, 0, 30):
            return 'suck'
        elif _utils.in_range(position, 30, 50):
            return 'buy'
        elif _utils.in_range(position, 50, 65):
            return 'hold'
        elif _utils.in_range(position, 65, 75):
            return 'sell'
        elif _utils.in_range(position, 75):
            return 'out'
    else:
        return 'shit'


if __name__ == '__main__':
    if len(argv) > 1:
        while True:
            print(format_index(get_status()))
            time.sleep(5)
    else:
        # format_index(get_status())
        wave_df = wave.get_wave(codes=target, start='2015-01-01', is_index=True)
        print(wave_df)
        # plot figure
        list_df = []
        for code in target:
            wdf = wave_df[wave_df.code == code]
            list_df.append(wave.format_wave_data(wdf, is_index=True), )
        # figure display
        wave.plot_wave(list_df, filename='wave_index.png', columns=3)

