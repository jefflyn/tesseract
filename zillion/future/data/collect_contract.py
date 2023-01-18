import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from zillion.future.domain import contract, basic
from zillion.future.future_util import get_future_basics
from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

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
        for mc in main_contracts:
            symbol = symbol_varieties(mc)
            main_contract_map[symbol] = mc
            if symbol in basic_symbols and mc not in contract_code:
                ts_code = mc + '.' + symbol_exchange.get(symbol)
                contract.save_contract([[symbol, mc, ts_code, 1, 0, 0, None, None, 1,
                                         date_util.now(), date_util.now(), 0]])
    print(main_contract_map)
    if len(contract_code) == 0:
        print('done!!!')
    for index, row in contract_df.iterrows():
        symbol = row['symbol']
        code = row['code']
        not_main = row['main'] != 1
        main_code = main_contract_map.get(symbol)
        if main_code is None:
            print('No symbol found, please check!!! >>> ', symbol)
            continue
        if symbol not in basic_symbols or code < main_code:
            contract.remove_contract_hist(code, [list(row.values)])
            print("remove ", code)
        if code == main_code and not_main:
            contract.update_contract_main(code)
