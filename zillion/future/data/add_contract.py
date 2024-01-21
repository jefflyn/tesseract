import pandas as pd
from akshare.futures.symbol_var import symbol_varieties

from zillion.future.data.collect_contract import update_contract_hl
from zillion.future.domain import contract, daily
from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    code = 'SF2405'
    time_now = date_util.now()
    contract_df = contract.get_local_contract()
    contract_codes = list(contract_df['code'])
    main_contract_map = dict()
    if code not in contract_codes:
        contract_df = contract_df[contract_df.symbol == symbol_varieties(code)].head(1)
        ts_code = contract_df.at[contract_df.index.to_numpy()[0], 'ts_code']
        h_low = contract_df.at[contract_df.index.to_numpy()[0], 'h_low']
        h_high = contract_df.at[contract_df.index.to_numpy()[0], 'h_high']
        h_low_time = contract_df.at[contract_df.index.to_numpy()[0], 'h_low_time']
        h_high_time = contract_df.at[contract_df.index.to_numpy()[0], 'h_high_time']

        contract.save_contract([[symbol_varieties(code), code, code + '.' + ts_code.split('.')[1], 1, 0, 0, '', '',
                                 h_low, h_high, h_high_time, '', 1,
                                 time_now, time_now, 0]])
        print("add new contract hist daily:", code)
        daily.collect_hist_daily_ak([code])
        update_contract_hl(code)
