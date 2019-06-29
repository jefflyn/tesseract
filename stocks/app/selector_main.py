from stocks.data import data_util
from stocks.app import selector
from stocks.base.logging import logger
import stocks.base.display

if __name__ == '__main__':
    logger.info('start selector main ...')
    # ##select from all
    # selector.select_from_all()

    # selector.select_result(['002918'], 'temp')

    # ##select from wave
    codes = data_util.get_codes_by_wave()
    selector.select_result(codes, 'wave')

    # ##select from region
    # codes = data_util.get_codes_by_region(region='佛山')
    # selector.select_result(codes, 'region')

    # ##select from ma
    # code_df = data_util.get_ma_code('d')
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'ma_d')

    # ##select from limitup
    # type = 'm'
    # period = '2019-02'
    # code_df = data_util.get_limitup_code(period_type=type, period=period, times=3)
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'limitup_' + period)

    # ##select from concepts -大基建、大消费、大金融、大健康、大科技、大军工
    # concept_codes = data_util.get_code_by_concept('风电')
    # selector.select_result(concept_codes, 'concept')

    # ##select by new
    # selector.select_from_subnew(fname='new')

    # selector.select_from_change_week()
    # selector.select_from_change_month()

    # sql = "select code from profit_forecast where type in ('预增', '预盈') and range_from > 100"
    # codes = data_util.get_codes_from_sql(sql)
    # selector.select_result(codes, 'forecast')








