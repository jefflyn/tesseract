import akshare as ak
import pandas as pd

from zillion.future import db_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
db_util.to_db(stock_zh_a_spot_em_df, 'stock_a_list', if_exists='replace', db_name='stock')

print(stock_zh_a_spot_em_df)