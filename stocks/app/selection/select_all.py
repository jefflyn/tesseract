from stocks.data import data_util
from stocks.app.selection import selector


if __name__ == '__main__':
    print('start selector main ...')
    # >>> select from all
    selector.select_from_all()

    # >>> select from wave
    # codes = data_util.get_codes_by_wave()
    # selector.select_result(codes, 'wave')