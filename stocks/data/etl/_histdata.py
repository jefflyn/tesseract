import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

import stocks.base.dateutils as dateutil
from stocks.base.logging import logger
from stocks.data import _datautils as _dt
import stocks.base.dateconst as dconst

pd.set_option('display.width', 800)


def hist_data_month_extract(n=6):
    """
    use for getting 6 months' change data
    t+0, none type price and faster than get_h_data
    :return: date open high close low volume price_change p_change ma5 ma10 ma20 v_ma5 v_ma10 v_ma20
    """
    results = pd.DataFrame()
    codes = _dt.get_all_codes(excludeCyb=True)
    logger.info('total size %d' %len(codes))
    total_size = 0
    for code in codes:
        histdf = ts.get_hist_data(code=code, ktype='M', start=dconst.LAST_DAY_6_MONTH)
        if histdf is not None and len(histdf) > 0:
            total_size += 1
            histdf['date'] = histdf.index
            histdf['code'] = code
            results = results.append(histdf, ignore_index=True)
    logger.info('final extract size %d' %total_size)
    _dt.to_db(results, 'hist_data_month')


if __name__ == '__main__':
    logger.info('__main__')
    hist_data_month_extract()
    # view_notices_content()
    # histdf = ts.get_hist_data(code='000710', ktype='M', start=dconst.LAST_DAY_6_MONTH)
    # histdf['code'] = '000710'
    # histdf['date'] = histdf.index
    #
    # rr = histdf.pivot(index='code', columns='date', values='p_change')
    # print(histdf)
    # print(rr)
