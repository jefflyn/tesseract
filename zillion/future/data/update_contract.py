import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from utils.datetime import date_util
from zillion.future.domain import contract, basic, daily, gap
from zillion.future.future_constants import EXCHANGE_ALIAS_MAP

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def update_contract_hl(code):
    daily_df = daily.get_daily(code)
    row1 = _update_contract_hl(code, daily_df)

    #####
    c_code = symbol_varieties(code) + '0'
    c_daily_df = daily.get_daily(c_code)
    row2 = _update_contract_hl(code, c_daily_df, update_hist=True)
    return row1 + row2


def _update_contract_hl(code, daily_df, update_hist=False):
    low_list = list(daily_df['low'])
    high_list = list(daily_df['high'])
    if len(low_list) == 0 or len(high_list) == 0:
        return
    date_list = list(daily_df['trade_date'])
    lowest = min(low_list)
    lowest_date = date_list[low_list.index(lowest)]
    highest = max(high_list)
    highest_date = date_list[high_list.index(highest)]
    return contract.update_hl(code, lowest, lowest_date, highest, highest_date, update_hist)


if __name__ == '__main__':
    time_now = date_util.now()
    contract_df = contract.get_local_contract()
    for index, row in contract_df.iterrows():
        code = row['code']
        daily_df = daily.get_daily(code)
        if daily_df is None or daily_df.empty:
            print(code, '数据缺失')
        update_contract_hl(code)
    print(time_now)