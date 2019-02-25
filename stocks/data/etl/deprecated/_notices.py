"""
公告数据
Created on 2018/07/16
@author: linjingu
@group : guru.com
"""

import pandas as pd
import stocks.base.date_const as dconst
import stocks.base.db_util as _dt
import tushare as ts
from stocks.base.logging import logger
from stocks.data import data_util

pd.set_option('display.width', 800)


def notices_extract():
    notices_extract_result = pd.DataFrame()
    codes = data_util.get_all_codes(excludeCyb=True)
    logger.info('total size %d' % len(codes))
    total_size = 0
    for code in codes:
        notices = ts.get_notices(code=code, date=dconst.TODAY)
        if notices is None or notices.empty is True:
            continue
        ++total_size
        notices.insert(0, 'code', code)
        notices_extract_result = notices_extract_result.append(notices, ignore_index=True)

    logger.info('final extract size %d' % total_size)
    if notices_extract_result.empty is False:
        _dt.to_db(notices_extract_result, 'notices', if_exists='append')


if __name__ == '__main__':
    logger.info('__main__')
    notices_extract()
