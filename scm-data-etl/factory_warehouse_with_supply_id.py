import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import pymysql

oss_db = pymysql.connect(host='rm-2ze886b0r63l4127w605.mysql.rds.aliyuncs.com', user='oss',
                         passwd='JdmPi2URFCWyIaTh', db='oss', charset='utf8')

jiuhua_db = pymysql.connect(host='rm-2ze886b0r63l4127w605.mysql.rds.aliyuncs.com', user='jiuhua',
                            passwd='qhTzegR2Ju0lgURa', db='jiuhua', charset='utf8')

cursor = oss_db.cursor()
scm_supplier_sql = "select id, short_name from scm_supplier where short_name <> ''"
result = cursor.execute(scm_supplier_sql)
print(result)
scm_supplier = cursor.fetchall()
scm_supplier_map = dict()
for t in scm_supplier:
    scm_supplier_map[t[1]] = t[0]
    scm_supplier_map[t[1][:2]] = t[0]
print(scm_supplier_map)

jiuhua_cursor = jiuhua_db.cursor()
factory_warehouse_sql = "select id, name from warehouse where position_type = 1"
result2 = jiuhua_cursor.execute(factory_warehouse_sql)
print(result2)
for warehouse in jiuhua_cursor.fetchall():
    id = warehouse[0]
    name = str(warehouse[1])
    for i in range(len(name)):
        filter_name = name[i:(i + 2)]
        supplier_id = scm_supplier_map.get(filter_name)
        if supplier_id is not None:
            update_sql = "update warehouse set owner_agent_id=" + str(supplier_id) + " where id=" + str(id)
            jiuhua_cursor.execute(update_sql)
            break
jiuhua_db.commit()
