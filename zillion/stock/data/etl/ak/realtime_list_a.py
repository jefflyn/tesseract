import akshare as ak
import pandas as pd

from zillion.utils import db_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

df = ak.stock_zh_a_spot_em()
# 过滤价格null
result = df.loc[df['最新价'].notnull()]
db_util.to_db(result, 'realtime_list_a', if_exists='replace', db_name='stock')

print(result)