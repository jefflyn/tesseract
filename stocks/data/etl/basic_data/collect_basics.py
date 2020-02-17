# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
股票基本数据，每天采集
Created on 2019/02/07
@author: guru
"""
import tushare as ts
import pandas as pd
from stocks.util.db_util import get_db
from stocks.util._utils import timer
from stocks.util import date_util


@timer
def collect_basics():
    stock_basics = ts.get_stock_basics()
    stock_basics['code'] = stock_basics.index
    insert_values = []
    trade_date = date_util.get_latest_trade_date(1)[0]
    import numpy as np
    for index, row in stock_basics.iterrows():
        code = row['code']
        ts_code = code + '.SH' if code[:1] == '6' else code + '.SZ'
        curt_values = (trade_date, code, ts_code, row['name'], row['industry'], row['area'], row['pe'],
                       row['outstanding'], row['totals'], row['totalAssets'], row['liquidAssets'], row['fixedAssets'],
                       row['reserved'], row['reservedPerShare'], row['esp'], row['bvps'], row['pb'], row['timeToMarket'],
                       row['undp'], row['perundp'], row['rev'], row['profit'], row['gpr'], row['npr'], row['holders'])
        insert_values.append(tuple(np.nan_to_num(curt_values)))
    total_size = len(insert_values)

    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    try:
        cursor.execute("delete from basics")
        # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
        insert_count = cursor.executemany('insert into basics(trade_date,code,ts_code,name,industry,area,pe,circulate_shares,'
                                          'total_shares,total_assets,liquid_assets,fixed_assets,reserved,reserved_per_share,'
                                          'esp,bvps,bp,list_date,undp,undp_per_share,revenue,profit,gpr,npr,holders) '
                                          'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                                          '%s,%s,%s,%s,%s,%s,%s)', insert_values)
        db.commit()
        print(trade_date, 'All Finished! Total size: ' + str(total_size) + ' , ' + str(insert_count) + ' insert successfully.')
    except Exception as err:
        print('>>> failed!', err)
        db.rollback()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    collect_basics()



