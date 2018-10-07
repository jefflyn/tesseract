"""
公告数据
Created on 2018/07/16
@author: linjingu
@group : guru.com
"""

import pandas as pd
import stocks.base.dateconst as dconst
import stocks.base.dbutils as _dt
import tushare as ts
from stocks.base.logging import logger
from stocks.data import _datautils

pd.set_option('display.width', 800)



def get_notices_code(content=None):
    notice_df = None
    notice_df = _dt.read_query('select code, title from notices')
    if content is not None:
        notice_df = notice_df[notice_df.title.str.contains(r'.*?' + content + '*')]
    notice_df = notice_df.drop_duplicates(['code'])
    logger.info('total size: %d' % len(notice_df.index))
    return list(notice_df['code'])



if __name__ == '__main__':
    logger.info('__main__')
    get_notices_code('重大资产重组')
