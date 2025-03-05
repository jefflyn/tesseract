import akshare as ak
import pandas as pd
from akshare.futures.cons import market_exchange_symbols
from akshare.futures.symbol_var import symbol_varieties

from utils.datetime import date_util
from zillion.future.data.update_contract import update_contract_hl
from zillion.future.domain import contract, basic, daily, gap
from zillion.future.future_constants import EXCHANGE_ALIAS_MAP

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)



if __name__ == '__main__':
    time_now = date_util.now()
    basic_df = basic.get_all()
    symbol_list = list(basic_df['symbol'])
    symbol_exchange_map = basic.symbol_exchange_map(basic_df)
    contract_df = contract.get_local_contract()
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
            deleted_symbol = basic_df.loc[symbol, 'deleted']
            if deleted_symbol == 1:
                contract.remove_contract_hist(main_code, None)
                continue

            main_contract_map[symbol] = main_code
            if main_code not in contract_codes:
                ts_code = main_code + '.' + exchange_ts
                limit = basic_df.loc[symbol, 'limit']
                contract.save_contract([[symbol, main_code, ts_code, 1, limit, 0, 0, '', '', 0, 0, '', '', 1,
                                         time_now, time_now, 0]])
                print("  >>> add new contract hist daily:", main_code)
                daily.collect_hist_daily_ak([main_code])

            if symbol not in symbol_list:
                print(symbol, "add to basic")
                basic.add_basic([symbol, '', exchange_ts, time_now])
            update_contract_hl(main_code)

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
            contract.remove_contract_hist(code, [list(row.values)])
            gap.del_gap_record(code)
            daily.delete_daily(code)
            continue

        daily_df = daily.get_daily(code)
        if daily_df is None or daily_df.empty:
            daily.collect_hist_daily_ak([code])
            # wave.redo_wave()
        if code > main_code:
            update_contract_hl(code)
        if code == main_code and not_main is True:
            contract.update_contract_main(code)
    print(time_now)