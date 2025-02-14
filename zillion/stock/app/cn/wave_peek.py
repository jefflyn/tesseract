from datetime import datetime

import numpy as np
import pandas as pd

from zillion.db.DataSourceFactory import session_stock
from zillion.stock.dao.daily_quote_dao import DailyQuoteDAO
from zillion.utils.wave_util import get_wave, wave_to_str, get_wave_ab, get_wave_ab_fast


def wave_test(code=None):
    daily_quote_dao = DailyQuoteDAO(session_stock)
    hist_data = daily_quote_dao.get_daily_a(code)
    result = get_wave(code, hist_data)
    print(result)
    wave_str = wave_to_str(result)
    print(wave_str)
    wave_ab = get_wave_ab(wave_str, 33)
    print(wave_ab)
    print('get_wave_ab_fast', get_wave_ab_fast(wave_str))


if __name__ == '__main__':
    wave_test(code='300598')
