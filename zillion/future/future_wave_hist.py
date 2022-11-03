import pandas as pd

from zillion.future import future_util
from zillion.future import future_wave
from zillion.utils import db_util

pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    # tscode = 'CF2101.ZCE,CF2105.ZCE,CF2109.ZCE,CF2201.ZCE,CF2205.ZCE,CF2209.ZCE'
    # ts_code_list = tscode.split(",")
    ts_code_list = ['CF2105.ZCE', 'CF2109.ZCE', 'CF2201.ZCE', 'CF2205.ZCE', 'CF2309.ZCE', 'CF2301.ZCE', 'CF2303.ZCE', 'CF2305.ZCE', 'CF2307.ZCE', 'CF2309.ZCE']

    wave_data_list = []
    for code in ts_code_list:
        df_data = future_util.get_ts_future_hist_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print("no daily data found!")
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        wave_df = future_wave.get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)
        wave_str = future_wave.wave_to_str(wave_df)
        if wave_str == '':
            print(code)
        wave_list = future_wave.get_wave_list(wave_str)
        wave_list.insert(0, code)
        wave_list.insert(1, code.split('.')[0])
        wave_list.insert(2, list(wave_df['begin'])[0])
        wave_list.insert(3, list(wave_df['end'])[-1])
        print(wave_df)
        print(wave_str)
        print(wave_list)
        wave_data_list.append(wave_list)
    wave_df_result = pd.DataFrame(wave_data_list,
                                  columns=['ts_code', 'code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp',
                                           'dp'])
    db_util.to_db(wave_df_result, 'future_wave_hist')
