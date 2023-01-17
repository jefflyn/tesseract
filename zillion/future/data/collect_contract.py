import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from zillion.future.domain import contract
from zillion.future.future_util import get_future_basics

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    basics = get_future_basics()
    basic_symbols = list(basics['symbol'])
    main_contract_map = dict()
    for key in market_exchange_symbols.keys():
        match_main_contract_df = ak.match_main_contract(symbol=key)
        main_contracts = match_main_contract_df.split(",")
        for mc in main_contracts:
            main_contract_map[symbol_varieties(mc)] = mc
    print(main_contract_map)
    df = contract.get_local_contract()
    for index, row in df.iterrows():
        symbol = row['symbol']
        code = row['code']
        if symbol not in basic_symbols:
            contract.remove_contract_hist(code, [row.values])
            print("remove ", code)




