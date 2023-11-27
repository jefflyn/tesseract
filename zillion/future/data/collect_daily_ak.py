import pandas as pd

from zillion.future.domain import contract, daily
from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    trade_date = date_util.get_today()
    # trade_date = '2023-01-20'
    # 连续
    code_list = contract.get_0_contract_code()
    daily.collect_daily_ak(code_list, trade_date)

    contract_df = contract.get_local_contract()
    code_list = list(contract_df['code'])
    daily.collect_daily_ak(code_list, trade_date)

    print('done @', date_util.now_str())
