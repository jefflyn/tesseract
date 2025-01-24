from datetime import datetime

import numpy as np
import pandas as pd

import zillion.utils.db_util as _dt
from utils.datetime import date_util
from zillion.future.domain import trade, contract, daily
from zillion.utils import wave_util


def add_realtime_data(code=None, local_last_trade_date=None):
    last_trade_date = date_util.get_today()  # .get_latest_trade_date(1)[0]
    if local_last_trade_date < last_trade_date:  # not the latest record
        realtime = trade.realtime_simple(code.split('.')[0])
        if realtime is not None and realtime.empty is False:
            realtime['code'] = code
            return realtime
    return None


def wave_to_db(wave_list=None, wave_detail_list=None):
    wave_df_result = pd.DataFrame(wave_list,
                                  columns=['code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp', 'dp',
                                           'p'])
    wave_df_result['update_time'] = date_util.now()
    _dt.to_db(wave_df_result, tb_name='wave', db_name='future')
    wave_detail_result = pd.DataFrame(pd.concat(wave_detail_list),
                                      columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price',
                                               'change', 'days'])
    _dt.to_db(wave_detail_result, tb_name='wave_detail', db_name='future')


def get_high_low():
    df = _dt.read_query('future','select code, GREATEST(ap, bp, cp, dp) high, LEAST(ap, bp, cp, dp) low from wave')
    df.index = list(df['code'])
    return df


def redo_wave():
    print(date_util.now_str())
    ############################################################
    mian_codes = contract.get_0_contract_code()
    codes = list(contract.get_local_contract()['code'])
    code_list = mian_codes + codes
    ############################################################
    # code_list = ['FG0']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    size = len(code_list)
    for code in code_list:
        df_data = daily.get_daily(code)[['code', 'trade_date', 'open', 'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        # df_data['code'] = df_data['code'].apply(lambda x: str(x).split('.')[0])
        wave_df = wave_util.get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)
        wave_detail_list.append(wave_df)
        wave_str = wave_util.wave_to_str(wave_df)
        wave_list = wave_util.get_wave_list(wave_str)
        wave_list.append(wave_df.tail(1).iloc[0, 5])  # end_price
        wave_list.insert(0, code)
        wave_list.insert(1, list(wave_df['begin'])[0])
        wave_list.insert(2, list(wave_df['end'])[-1])
        wave_data_list.append(wave_list)
        # print(result)
        # print(wave_str)
        # wave_ab = get_wave_ab(wave_str, 33)
        # print(wave_ab)
        # print('get_wave_ab_fast', get_wave_ab_fast(wave_str))
        print(size, code)
        size = size - 1

    wave_to_db(wave_data_list, wave_detail_list)
    print(date_util.now_str())


if __name__ == '__main__':
    redo_wave()
