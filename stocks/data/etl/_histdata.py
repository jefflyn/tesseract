import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

import stocks.base.dateutils as dateutil
from stocks.base.logging import logger
from stocks.data import _datautils
import stocks.base.dbutils as _dt
import stocks.base.dateconst as dconst

pd.set_option('display.width', 800)


def hist_data_month_extract(n=6):
    """
    get_hist_data func use for getting 6 months' change data
    t+0, none type price and faster than get_h_data
    :return: date open high close low volume price_change p_change ma5 ma10 ma20 v_ma5 v_ma10 v_ma20
    """
    hist_results = pd.DataFrame()
    change_results = pd.DataFrame()
    codes = _datautils.get_all_codes(excludeCyb=True)
    logger.info('total size %d' %len(codes))
    total_size = 0
    date_lists = [dconst.shift_date(target=dconst.parse_datestr(dconst.LAST_DAY_6_MONTH), shiftType='m', n=x, format=dconst.DATE_FORMAT_MONTH) for x in range(n+1)]
    for code in codes:
        histdf = ts.get_hist_data(code=code, ktype='M', start=dconst.LAST_DAY_6_MONTH)
        if histdf is not None and histdf.empty is False:
            total_size += 1
            histdf['date'] = histdf.index
            histdf['code'] = code
            hist_results = hist_results.append(histdf, ignore_index=True)
            hist_change = histdf[['code', 'date', 'p_change']]
            hist_change['date'] = hist_change['date'].apply(lambda x: dconst.parse_datestr(x, dconst.DATE_FORMAT_MONTH))

            default_change = pd.DataFrame()
            default_change['date'] = date_lists
            default_change['code'] = code
            default_change['change'] = 0.0

            #default_change dataframe join the hist_change dataframe
            merge_result = pd.merge(default_change, hist_change, on=['code', 'date'], how='left')
            merge_result = merge_result.fillna(0.0)
            change_results = change_results.append(merge_result[['code', 'date', 'p_change']], ignore_index=True)

    logger.info('final extract size %d' %total_size)
    _dt.to_db(hist_results, 'hist_data_month')
    _dt.to_db(change_results, 'hist_change_month')


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
