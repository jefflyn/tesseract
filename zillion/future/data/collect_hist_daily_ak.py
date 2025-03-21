import pandas as pd

from utils.datetime import date_util
from zillion.future.domain import daily, contract

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    contract_df = contract.get_local_contract()
    # 主力
    code_list = list(contract_df['code'])
    # daily.collect_hist_daily_ak(code_list)
    # daily.collect_hist_daily_ak(codes=code_list, trade_date='2025-03-19')

    # 连续
    code_list = contract.get_0_contract_code()
    # code_list = ['PS0']
    # daily.collect_hist_daily_ak(codes=code_list)
    # daily.collect_hist_daily_ak(codes=code_list, trade_date='2025-03-19')
    print('done @', date_util.now_str())
