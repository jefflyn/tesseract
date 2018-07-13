import datetime as dt
from datetime import datetime

import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils as _dt
from stocks.base.logging import logger


def view_concept_classified():
    df = ts.get_concept_classified()
    _dt.to_db(df, 'concept')
    logger.info(df)


def view_h_data():
    """
    t+1, slow,
    :return: date open high close low volume amount
    """
    hdf = ts.get_h_data(code='603676')
    logger.info(hdf)


def view_hist_data():
    """
    use for getting every k type change data
    t+0, none type price and faster than get_h_data
    :return: date open high close low volume price_change p_change ma5 ma10 ma20 v_ma5 v_ma10 v_ma20
    """
    histdf = ts.get_hist_data(code='603676', ktype='M')
    logger.info(histdf)


def view_k_data():
    """
    use for getting every type price data of every k type
    t+0, very fast
    :return: date open close high low volume code
    """
    kdf = ts.get_k_data(code='603676')
    logger.info(kdf)


def view_notices():
    notices = ts.get_notices(code='000593', date='2018-07-01')
    _dt.to_db(notices, 'notices')
    logger.info(notices)


def view_notices_content():
    notice_content = ts.notice_content(url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?CompanyCode=10000930&gather=1&id=4574299')
    logger.info(notice_content)


if __name__ == '__main__':
    logger.info('__main__')
    view_notices()
    # view_notices_content()
