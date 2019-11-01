import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import pymysql


pre_db = pymysql.connect(host='mysql-pre.dian.so', user='pre_user', passwd='CPE0SbDLgvDO9j3n', charset='UTF8MB4')

pre_cursor = pre_db.cursor()
purchase_order_sql = "select * from oss.agent_purchase_order where status in (1,3)"
result = pre_cursor.execute(purchase_order_sql)
purchase_order = pre_cursor.fetchall()
print(purchase_order)

#
# scm_supplier = cursor.fetchall()
# scm_supplier_map = dict()
# for t in scm_supplier:
#     scm_supplier_map[t[1]] = t[0]
#     scm_supplier_map[t[1][:2]] = t[0]
# print(scm_supplier_map)
#
# jiuhua_cursor = jiuhua_db.cursor()
# factory_warehouse_sql = "select id, name from warehouse where position_type = 1"
# result2 = jiuhua_cursor.execute(factory_warehouse_sql)
# print(result2)
# for warehouse in jiuhua_cursor.fetchall():
#     id = warehouse[0]
#     name = str(warehouse[1])
#     for i in range(len(name)):
#         filter_name = name[i:(i + 2)]
#         supplier_id = scm_supplier_map.get(filter_name)
#         if supplier_id is not None:
#             update_sql = "update warehouse set owner_agent_id=" + str(supplier_id) + " where id=" + str(id)
#             jiuhua_cursor.execute(update_sql)
#             break
# jiuhua_db.commit()
