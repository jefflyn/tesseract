from stocks.data import data_util
from stocks.app import selector
from stocks.base.logging import logger
import stocks.base.display

if __name__ == '__main__':
    logger.info('start selector main ...')
    ### 全量
    # selector.select_from_all()

    # ###移动平均
    # code_df = data_util.get_ma_code('d')
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'ma_d')

    # ###select from limitup
    # type = 'm'
    # period = '2018-11'
    # code_df = data_util.get_limitup_code(period_type=type, period=period, times=3)
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'limitup_' + period)

    # ###select from concepts
    concept_codes = data_util.get_code_by_concept('粤')
    selector.select_result(concept_codes, 'concept')

    # ##select by new
    selector.select_from_subnew(fname='new')

    # selector.select_from_change_week()
    # selector.select_from_change_month()











