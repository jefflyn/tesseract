import pandas as pd
import json

# 读取json文件 JSON
df = pd.read_json("raz_list.json")

# 打印表格
print(df.to_string(index=False))

df.to_csv("raz_list.csv")