import mysql.connector
import json

# 1、连接数据库并查询 java_nav_data 和 java_nav_display 表
conn = mysql.connector.connect(
    host="localhost",  # 数据库主机
    user="linjingu",       # 数据库用户名
    password="linjingu",  # 数据库密码
    database="app"  # 数据库名称
)

cursor = conn.cursor(dictionary=True)

# 查询 java_nav_data 表
cursor.execute("SELECT id, title, style, details, sub_items FROM java_nav_data WHERE deleted = 0")
data_rows = cursor.fetchall()

# 查询 java_nav_display 表
cursor.execute("SELECT type, column_1, column_2, column_3, column_4, column_5, column_6 FROM java_nav_layout")
layout_rows = cursor.fetchall()

# 关闭数据库连接
cursor.close()
conn.close()

# 2、转换 java_nav_data 数据为 DATA_MAP
data_map = {}
for row in data_rows:
    sub_items = row["sub_items"].split("\n") if row["sub_items"] else []

    data_map[row["id"]] = {
        "title": row["title"],
        "style": row["style"] or "",
        "details": row["details"] or "",
        "subItems": [item.strip() for item in sub_items if item.strip()]  # 去除空白项
    }

# 3、转换 java_nav_display 数据为 LAYOUT_MAP
# 构造 LAYOUT_MAP
layout_map = {}
for row in layout_rows:
    if row["type"] not in layout_map:
        layout_map[row["type"]] = []

    # 处理每一行，过滤空值
    layout_map[row["type"]].append([
        row["column_1"],
        row["column_2"],
        row["column_3"],
        row["column_4"],
        row["column_5"],
        row["column_6"]
    ])

#4、导出为 data.js 文件
# 生成最终的 JavaScript 文件内容
js_content = f"""
const DATA_MAP = {json.dumps(data_map, indent=2)};
const DISPLAY_MAP = {json.dumps(layout_map, indent=2)};
"""

# 将生成的 JS 写入文件
with open("data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("JavaScript 文件已生成：data.js")
