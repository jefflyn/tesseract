from stocks.future import future_util
from stocks.future import future_wave

if __name__ == '__main__':
    code = 'SR2205.ZCE'
    df_data = future_util.get_ts_future_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
    df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
    wave_df = future_wave.get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)

    wave_str = future_wave.wave_to_str(wave_df)
    wave_list = future_wave.get_wave_list(wave_str)
    print(wave_str)
    print(wave_list)