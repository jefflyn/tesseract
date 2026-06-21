from utils.datetime import date_util
from utils.datetime.date_util import FORMAT_FLAT
from zillion.future.dao.contract_dao import ContractDAO
from zillion.future.domain import daily

if __name__ == '__main__':
    contract_dao = ContractDAO('future_sqlite')
    contract_df = contract_dao.get_all_contracts_as_df()

    code_list = list(contract_df['code'])
    # df = daily.fetch_daily_ak(code_list, trade_date='2026-06-17')
    df = daily.fetch_daily_ak(code_list, trade_date=date_util.get_today(FORMAT_FLAT))
    print(df)