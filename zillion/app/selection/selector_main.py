from zillion.app.selection import selector


if __name__ == '__main__':
    print('start selector main ...')
    # selector.select_result(['002892'], 'temp')

    # ##selection from all
    selector.select_from_all()

    # ##selection from wave
    # codes = data_util.get_codes_by_wave()
    # selector.select_result(codes, 'wave')

    # ##selection from region
    # codes = data_util.get_codes_by_region(region='佛山')
    # selector.select_result(codes, 'region')

    # ##selection from concepts -大基建、大消费、大金融、大健康、大科技、大军工
    # concept_codes = data_util.get_code_by_concept('基建')
    # selector.select_result(concept_codes, 'concept')

    # ##selection from ma
    # code_df = data_util.get_ma_code('d')
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'ma_d')

    # ##selection from limitup
    # type = 'm'
    # period = '2019-02'
    # code_df = data_util.get_limitup_code(period_type=type, period=period, times=3)
    # codes = list(code_df['code'])
    # selector.select_result(codes, 'limitup_' + period)

    # ##selection by new
    # selector.select_from_subnew(fname='new')

    # selector.select_from_change_week()
    # selector.select_from_change_month()

    # sql = "select code from profit_forecast where type in ('预增', '预盈') and range_from > 100"
    # codes = data_util.get_codes_from_sql(sql)
    # selector.select_result(codes, 'forecast')








