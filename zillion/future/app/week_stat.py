import pandas as pd

from zillion.future.domain import daily, contract
from zillion.utils import db_util

if __name__ == '__main__':
    contracts = contract.get_local_contract()
    week_start = '2024-11-11'
    week_end = '2024-11-15'
    week_stat_data = []
    for index, row in contracts.iterrows():
        code = row['code']
        print('processing ', code)
        df_data = daily.get_daily(code, start_date=week_start,
                                                  end_date=week_end)[
            ['code', 'trade_date', 'pre_close', 'pre_settle', 'open', 'high', 'low', 'close']]
        pre_close_data = list(df_data['pre_close'])
        close_data = list(df_data['close'])
        pre_close = pre_close_data[0]
        close = close_data[-1]
        week_change = round((close - pre_close) * 100 / pre_close, 2)
        week_stat_data.append([row['code'], week_end, round(close - pre_close, 1), float(week_change)])
    wave_df_result = pd.DataFrame(week_stat_data, columns=['code', 'week', 'change', 'pct_change'])
    db_util.to_db(wave_df_result, 'week_stat', if_exists='append', db_name='future')
