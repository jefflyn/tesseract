# !/usr/bin/env python
# -*- coding: utf-8 -*-

from stocks.util.pro_util import pro

if __name__ == '__main__':
    # 获取CU2007合约期间行情
    df = pro.fut_daily(ts_code='CU2007.SHF', start_date='20200101', end_date='20201113')
    print(df)

    # 获取某日期大商所全部合约行情数据
    df = pro.fut_daily(trade_date='20200930', exchange='DCE',
                       fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')
    print(df)