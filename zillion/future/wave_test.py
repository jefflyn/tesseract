import pandas as pd

from zillion.future import db_util
from zillion.future.app import wave
from zillion.future.domain import daily

pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    code_list = ['SA2309']

    wave_data_list = []
    for code in code_list:
        df_data = daily.get_daily(code)[['code', 'trade_date', 'open', 'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print("no daily data found!")
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        wave_df = wave.get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)
        wave_str = wave.wave_to_str(wave_df)
        if wave_str == '':
            print(code)
        wave_list = wave.get_wave_list(wave_str)
        wave_list.append(wave_df.tail(1).iloc[0, 5])  # end_price
        wave_list.insert(0, code)
        wave_list.insert(1, list(wave_df['begin'])[0])
        wave_list.insert(2, list(wave_df['end'])[-1])
        print(wave_df)
        print(wave_str)
        print(wave_list)
        wave_data_list.append(wave_list)
    wave_df_result = pd.DataFrame(wave_data_list,
                                  columns=['code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp', 'dp', 'p'])
    db_util.to_db(wave_df_result, 'wave_hist')
