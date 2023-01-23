import zillion.utils.db_util as _dt
from zillion.future.domain import contract, gap
from zillion.utils import date_util

if __name__ == '__main__':
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    main_code_list = contract.get_main_contract_code()

    contract_df = contract.get_local_contract()
    code_list = list(contract_df['code'])
    # 插入新的gap
    gap.add_gap(main_code_list + code_list)

    # 更新gap信息
    gap.update_gap()

    print('done @', date_util.get_now())
