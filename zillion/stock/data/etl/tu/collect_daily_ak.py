import akshare as ak

from zillion.future import db_util

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20180101", adjust="qfq")
db_util.to_db(stock_zh_a_hist_df, 'stock_a_daily', if_exists='replace', db_name='stock')

print(stock_zh_a_hist_df)