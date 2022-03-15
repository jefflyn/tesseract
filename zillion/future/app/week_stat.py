import pandas as pd

from zillion.future import future_util
from zillion.utils import db_util

if __name__ == '__main__':
    future_basics = future_util.get_future_basics()
    week_start = '20220314'
    week_end = '20220318'
    week_stat_data = []
    for index, row in future_basics.iterrows():
        code = row['code'] + '.' + row['exchange']
        df_data = future_util.get_ts_future_daily(code, start_date=week_start,
                                                  end_date=week_end)[
            ['ts_code', 'trade_date', 'pre_close', 'pre_settle', 'open', 'high', 'low', 'close']]
        pre_close_data = list(df_data['pre_close'])
        close_data = list(df_data['close'])
        pre_close = pre_close_data[0]
        close = close_data[-1]
        week_change = round((close - pre_close) * 100 / pre_close, 2)
        week_stat_data.append([row['code'], week_end, round(close - pre_close, 1), float(week_change)])
    wave_df_result = pd.DataFrame(week_stat_data, columns=['code', 'week', 'change', 'pct_change'])
    db_util.to_db(wave_df_result, 'future_week_stat', if_exists='append')
