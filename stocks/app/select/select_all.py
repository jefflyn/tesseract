from stocks.data import data_util
from stocks.app.select import selector
from stocks.util.logging import logger

if __name__ == '__main__':
    logger.info('start selector main ...')
    # >>> select from all
    selector.select_from_all()

    # ##select from wave
    codes = data_util.get_codes_by_wave()
    selector.select_result(codes, 'wave')
