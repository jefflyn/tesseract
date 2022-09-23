import tushare as ts

from zillion.utils import db_util

# 初始化pro接口
pro = ts.pro_api('f65316bb26b0a27ef7f876249615fcba99b5aab10e5be46cb278e53e')

# 拉取数据
df = pro.us_basic(**{
    "ts_code": "",
    "classify": "",
    "list_stauts": "",
    "offset": "18000",
    "limit": ""
}, fields=[
    "ts_code",
    "name",
    "classify",
    "list_date",
    "delist_date",
    "enname",
    "list_status"
])
print(df)
db_util.to_db(df, 'us_basic', if_exists='append')
