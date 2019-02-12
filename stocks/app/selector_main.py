from stocks.data import _datautils
from stocks.app import selector
from stocks.base.logging import logger
import stocks.base.display

if __name__ == '__main__':
    logger.info('start main')
    # selector.select_from_change_week()
    # selector.select_from_change_month()
    # selector.select_from_subnew(fname='new')
    # selector.select_from_all()
    # selector.select_from_concepts(CCONTS.RGZN, 'rgzn')
    # selector.select_from_industry(ICONTS.HXZY, 'hxzy')
    code_df = _datautils.get_ma_code('d')
    codes = list(code_df['code'])
    selector.select_result(codes, 'ma_d')
    # selector.select_result(_dt.get_monitor_codes('x'), 'x')
    # selector.select_result(notice.get_notices_code('股权转让'), 'notice_stock_transfer')
    # selector.select_result(notice.get_notices_code('重大资产重组'), 'notice_asset_reorg')
    # selector.select_result(_dt.get_code_by_industry('汽车配件'), 'qcpj')
    # selector.select_result(_dt.get_code_by_industry('互联网'), 'hlw')
    # selector.select_result(_dt.get_code_by_industry('食品'), 'sp')
    # selector.select_result(_dt.get_code_by_industry('化工原料'), 'hgyl')










