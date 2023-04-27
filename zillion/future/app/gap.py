from zillion.future.domain import contract, gap
from zillion.utils import date_util

if __name__ == '__main__':
    main_code_list = contract.get_main_contract_code()

    contract_df = contract.get_local_contract()
    code_list = list(contract_df['code'])
    # 插入新的gap
    gap.add_gap(main_code_list + code_list)

    # 更新gap信息
    gap.update_gap()

    print('done @', date_util.now_str())
