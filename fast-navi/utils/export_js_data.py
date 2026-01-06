from collections import defaultdict

import mysql.connector
import json

# 1、连接数据库并查询 java_nav_data 和 java_nav_display 表
conn = mysql.connector.connect(
    host="127.0.0.1",  # 数据库主机
    user="linjingu",  # 数据库用户名
    password="linjingu",  # 数据库密码
    database="app"  # 数据库名称
)

cursor = conn.cursor(dictionary=True)

# 查询 java_nav_data 表
cursor.execute("SELECT id, title, style, details, sub_items FROM java_nav_data WHERE deleted = 0")
data_rows = cursor.fetchall()

# 查询 java_nav_display 表
cursor.execute("SELECT type, row_index, col_index, data_id FROM java_nav_layout")
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
COLS = 6  # 固定 6 列

"""
rows: 查询出来的 java_nav_layout 记录
"""
layout_map = {}

grouped = defaultdict(list)
for r in layout_rows:
    grouped[str(r["type"])].append(r)

for type_, items in grouped.items():
    max_row_index = max(i["row_index"] for i in items)

    # 行数 = max_row_index + 1（因为从 0 开始）
    grid = [
        [None] * COLS
        for _ in range(max_row_index + 1)
    ]

    for i in items:
        r = i["row_index"]  # ✅ 不减 1
        c = i["col_index"]  # ✅ 不减 1
        grid[r][c] = i["data_id"]

    layout_map[type_] = grid


# 4、导出为 data.js 文件
# 生成最终的 JavaScript 文件内容
js_content = f"""
const DATA_MAP = {json.dumps(data_map, indent=2)};
const DISPLAY_MAP = {json.dumps(layout_map, indent=2)};
"""

# 将生成的 JS 写入文件
with open("data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("JavaScript 文件已生成：data.js")
