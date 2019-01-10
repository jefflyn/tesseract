import pandas as pd
from stocks.app import selector
from stocks.data import _datautils as _dt
from stocks.data.concept import constants as CCONTS
from stocks.data.industry import constants as ICONTS
from stocks.base.logging import logger
import stocks.data.etl.notices as notice

"""
don't commit this file
"""

pd.set_option('display.width', 2000)
pd.set_option('max_columns', 50)
pd.set_option('max_rows', 300)


if __name__ == '__main__':
    logger.info('start main')
    # selector.select_from_change_week()
    # selector.select_from_change_month()
    # selector.select_from_subnew(fname='subnew')
    # selector.select_from_all()
    # selector.select_from_concepts(CCONTS.RGZN, 'rgzn')
    # selector.select_from_industry(ICONTS.YS, 'ysjs')
    # selector.select_result(_dt.get_ot_codes(), 'ot')
    selector.select_result(_dt.get_app_codes(), 'app')
    # selector.select_result(_dt.get_monitor_codes('my'), 'my')
    # selector.select_result(notice.get_notices_code('股权转让'), 'notice_stock_transfer')
    # selector.select_result(notice.get_notices_code('重大资产重组'), 'notice_asset_reorg')
    # selector.select_result(_dt.get_code_by_industry('汽车配件'), 'qcpj')
    # selector.select_result(_dt.get_code_by_industry('互联网'), 'hlw')
    # selector.select_result(_dt.get_code_by_industry('食品'), 'sp')
    # selector.select_result(_dt.get_code_by_industry('化工原料'), 'hgyl')










