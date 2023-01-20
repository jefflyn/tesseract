from zillion.utils import db_util
from zillion.utils.pro_util import pro

if __name__ == '__main__':
    df_data = db_util.read_sql('select ts_code code, trade_date date, open, high, low, close from stock_daily order by trade_date', params={})
    if df_data is None or df_data.empty is True:
        df_data = pro.us_daily(ts_code='BABA')
        db_util.to_db(df_data, 'stock_daily')
    wave_df = future_wave.get_wave('BABA', hist_data=df_data, begin_low=True, duration=0, change=0)
    wave_str = future_wave.wave_to_str(wave_df)
    wave_list = future_wave.get_wave_list(wave_str)
    print(wave_df)
    print(wave_str)
    print(wave_list)
