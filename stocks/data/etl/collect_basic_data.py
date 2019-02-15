# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
股票基本数据，每7天采集一次
Created on 2019/01/01
@author: guru
"""

import pymysql

from stocks.base.pro_util import pro
from stocks.base.logging import logger
from stocks.base.dbutils import get_db

if __name__ == '__main__':
    # 查询当前所有正常上市交易的股票列表

    # 是否沪深港通标的，N否 H沪股通 S深股通
    data = pro.query('stock_basic', exchange='', list_status='',
                     fields='ts_code,symbol,name,area,industry,fullname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    total_size = data.shape[0]
    insert_count = 0
    for index, row in data.iterrows():
        try:
            sql_insert = "INSERT INTO basics(ts_code,code,name,area,industry,fullname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs) " \
                         "VALUES ('%s', '%s', '%s', '%s','%s','%s', '%s', '%s', '%s','%s','%s','%s','%s')" % \
                         tuple(row)
            result = cursor.execute(sql_insert)
            db.commit()
            insert_count += result
        except Exception as err:
            logger.error(err)
            continue

    # 关闭游标和数据库的连接
    cursor.close()
    db.close()
    logger.info('All Finished! Total size: ' + str(total_size) + ' , ' + str(insert_count) + ' insert successfully.')
