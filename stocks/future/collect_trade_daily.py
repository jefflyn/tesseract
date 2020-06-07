# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
股票基本数据，每7天采集一次
Created on 2019/01/01
@author: guru
"""

import pymysql

from stocks.util.pro_util import pro

from stocks.util.db_util import get_db

if __name__ == '__main__':
    # 获取CU2007合约期间行情
    df = pro.fut_daily(ts_code='CU2007.SHF', start_date='20200101', end_date='20201113')
    print(df)

    # 获取某日期大商所全部合约行情数据
    df = pro.fut_daily(trade_date='20200930', exchange='DCE',
                       fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')
    print(df)
