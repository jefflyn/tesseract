import pandas as pd

from zillion.future import future_util

pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    # tscode = 'CF2101.ZCE,CF2105.ZCE,CF2109.ZCE,CF2201.ZCE,CF2205.ZCE,CF2209.ZCE'
    # code_list = tscode.split(",")
    code_list = ['FG2301.ZCE']
    wave_data_list = []
    for code in code_list:
        df_data = future_util.get_ts_future_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                                                              'pre_close', 'pre_settle']]
        if df_data is None or df_data.empty:
            print("no daily data found!")
        df_data['change'] = (df_data["close"] - df_data["pre_close"]) * 100 / df_data["pre_close"]
        high_list = list(df_data['high'])
        low_list = list(df_data['low'])
        close_list = list(df_data['close'])
        change_list = list(df_data['change'])
        begin_idx = 0
        change_flag_idx = []
        for i in range(1, len(change_list)):
            change = change_list[i]
            if abs(change) > 1:
                change_flag_idx.append(i)


        print(change_flag_idx)

