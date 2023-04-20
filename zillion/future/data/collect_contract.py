import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from zillion.future.app import wave
from zillion.future.domain import contract, basic, daily, gap
from zillion.future.future_util import get_future_basics
from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def update_contract_hl(code):
    daily_df = daily.get_daily(code)
    low_list = list(daily_df['low'])
    high_list = list(daily_df['high'])
    date_list = list(daily_df['trade_date'])

    lowest = min(low_list)
    lowest_date = date_list[low_list.index(lowest)]
    highest = max(high_list)
    highest_date = date_list[high_list.index(highest)]
    rows = contract.update_contract_hl(code, lowest, lowest_date, highest, highest_date)
    if rows > 0:
        print("update contract hl:", code)


if __name__ == '__main__':
    basics = get_future_basics()
    basic_symbols = list(basics['symbol'])
    symbol_exchange = basic.symbol_exchange_map(basics)
    contract_df = contract.get_local_contract()
    contract_code = list(contract_df['code'])
    main_contract_map = dict()
    for key in market_exchange_symbols.keys():
        match_main_contract_df = ak.match_main_contract(symbol=key)
        main_contracts = match_main_contract_df.split(",")
        for main_code in main_contracts:
            symbol = symbol_varieties(main_code)
            main_contract_map[symbol] = main_code
            if symbol in basic_symbols and main_code not in contract_code:
                ts_code = main_code + '.' + symbol_exchange.get(symbol)
                contract.save_contract([[symbol, main_code, ts_code, 1, 0, 0, None, None, 1,
                                         date_util.now(), date_util.now(), 0]])
                print("add new contract hist daily:", main_code)
                daily.collect_hist_daily_ak([main_code])

                update_contract_hl(main_code)
    print(main_contract_map)
    if len(contract_code) == 0:
        print('done!!!')
    for index, row in contract_df.iterrows():
        symbol = row['symbol']
        code = row['code']
        not_main = row['main'] != 1
        main_code = main_contract_map.get(symbol)
        if symbol not in basic_symbols:
            continue
        if main_code is None:
            print('No main contract found, please check!!! >>> ', code)
            contract_df = contract.get_local_contract(symbol=symbol)
            if contract_df is None or contract_df.empty:
                continue
            code_list = list(contract_df['code'])
            for code in code_list:
                update_contract_hl(code)
            continue

        if symbol not in basic_symbols or code < main_code:
            contract.remove_contract_hist(code, [list(row.values)])
            gap.del_gap_record(code)
        daily_df = daily.get_daily(code)
        if daily_df is None or daily_df.empty:
            daily.collect_hist_daily_ak([code])
            wave.redo_wave()
        if code > main_code:
            update_contract_hl(code)
        if code == main_code and not_main is True:
            contract.update_contract_main(code)


