import pandas as pd

from zillion.future.domain import daily
from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    # 连续
    # code_list = contract.get_main_contract_code()
    # daily.collect_hist_daily_ak(code_list)
    #
    # contract_df = contract.get_local_contract()
    # code_list = list(contract_df['code'])
    code_list = ['SR2305']
    daily.collect_hist_daily_ak(code_list)
    print('done @', date_util.get_now())
