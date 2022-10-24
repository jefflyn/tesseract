# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('f65316bb26b0a27ef7f876249615fcba99b5aab10e5be46cb278e53e')

# 拉取数据
df = pro.fut_mapping(**{
    "ts_code": "SN.SHF",
    "trade_date": "",
    "start_date": "",
    "end_date": "",
    "limit": "",
    "offset": ""
}, fields=[
    # "ts_code",
    # "trade_date",
    "mapping_ts_code"
])
ts_codes = list(df['mapping_ts_code'])
new_list = list(dict.fromkeys(ts_codes))

print(new_list)

