# !/usr/bin/env python
# -*- coding: utf-8 -*-

from stocks.base import date_util
from stocks.base import db_util
from stocks.base.pro_util import pro
from stocks.base.logging import logger
from stocks.base.db_util import get_db
import sys

if __name__ == '__main__':
    """
    获取全部股票每日重要的基本面指标
    Created on 2019/02/01
    @author: guru
    """
    '''
        ts_code	str	TS股票代码
        trade_date	str	交易日期
        close	float	当日收盘价
        turnover_rate	float	换手率（%）
        turnover_rate_f	float	换手率（自由流通股）
        volume_ratio	float	量比
        pe	float	市盈率（总市值/净利润）
        pe_ttm	float	市盈率（TTM）
        pb	float	市净率（总市值/净资产）
        ps	float	市销率
        ps_ttm	float	市销率（TTM）
        total_share	float	总股本 （万）
        float_share	float	流通股本 （万）
        free_share	float	自由流通股本 （万）
        total_mv	float	总市值 （万元）
        circ_mv	float	流通市值（万元）
    '''
    hour = date_util.now.hour
    if hour < 10:
        sys.exit(0)
    trade_date = date_util.get_latest_trade_date(2, format=date_util.format_flat)
    for i in range(len(trade_date)):
        df = pro.query('daily_basic', ts_code='', trade_date=trade_date[i],
                       fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,'
                              'ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')

        if df is None or df.empty is True:
            logger.info(trade_date[i] + " no daily data found")
            continue
        df['code'] = df['ts_code'].apply(lambda x: x[0:6])
        db_util.to_db(df, 'basic_daily')
        logger.info('All Finished!')
        break
