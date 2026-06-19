import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from utils.datetime import date_util
from zillion.future.dao.basic_dao import BasicDAO
from zillion.future.dao.contract_dao import ContractDAO
from zillion.future.domain import contract, basic, daily, gap
from zillion.future.future_constants import EXCHANGE_ALIAS_MAP

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)



if __name__ == '__main__':
    time_now = date_util.now()

    basic_dao = BasicDAO('future_sqlite')
    contract_dao = ContractDAO('future_sqlite')

    basic_map = basic_dao.get_all_basic_as_map()
    print(f"   Count: {len(basic_map)}")
    symbol_list = list(basic_map.keys())

    contract_df = contract_dao.get_all_contracts_as_df()
    if contract_df.empty:
        contract_codes = []
    else:
        contract_codes = list(contract_df['code'])
    main_contract_map = dict()
    print('market exchange:', list(market_exchange_symbols.keys()))
    for key in market_exchange_symbols.keys():
        print('Exchange: <<<', key, '>>>')
        if 'cffex' == key:
            print(key, 'skip...')
            continue
        exchange_ts = EXCHANGE_ALIAS_MAP.get(key)
        match_main_contract_df = ak.match_main_contract(symbol=key)
        main_contracts = match_main_contract_df.split(",")
        for main_code in main_contracts:
            symbol = symbol_varieties(main_code)
            if symbol not in symbol_list:
                print(symbol, "not in basic. Error error error!!!")
                continue
            deleted_symbol = basic_map[symbol].deleted
            if deleted_symbol == 1:
                contract_dao.delete_contract(main_code, False)
                continue

            main_contract_map[symbol] = main_code
            if main_code not in contract_codes:
                contract_data = {
                    'symbol': symbol,
                    'code': main_code, 'low': 0, 'high':0,
                    'create_time': time_now,
                }
                contract_dao.insert_contract(contract_data)
                # print("  >>> add new contract hist daily:", main_code)
                # daily.collect_hist_daily_ak([main_code])

            if symbol not in symbol_list:
                print(symbol, "add to basic")
                basic_dict = {
                    'symbol': symbol,
                    'code': '',
                    'exchange': exchange_ts,
                    'time_now': time_now
                }
                basic_dao.insert_basic(basic_dict)
            # update_contract_hl(main_code)

    # print(main_contract_map)
    if len(contract_codes) == 0:
        print('done!!!')
    for index, row in contract_df.iterrows():
        symbol = row['symbol']
        code = row['code']
        not_main = row['main'] != 1
        main_code = main_contract_map.get(symbol)
        # symbol not in symbol_list or no main contract
        if main_code is None or code < main_code:
            contract_dao.delete_contract(code, False)
            continue
        if code == main_code and not_main is True:
            contract_dao.update_contract(code, {'main': 1})
    print(time_now)