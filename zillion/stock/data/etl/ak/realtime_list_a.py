import traceback

import akshare as ak
import pandas as pd

from zillion.db.DataSourceFactory import session_stock
from zillion.stock.dao.basic_a_dao import BasicADAO
from zillion.utils import db_util, date_util
from zillion.utils.date_util import now

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

df = ak.stock_zh_a_spot_em()
# 过滤价格null
result = df.loc[df['最新价'].notnull()]
db_util.to_db(result, 'realtime_list_a', if_exists='replace', db_name='stock')

print(result)

# 排序
result = result.sort_values(by='代码')

for index, row in result.iterrows():
    code = row['代码']
    basic_dao = BasicADAO(session_stock)
    basic = basic_dao.get_by_code(code)
    if basic is None:
        info = ak.stock_individual_info_em(symbol=code)
        if info is None or info.empty:
            print(code, 'stock info is empty...')
            continue
        try:
            industry = info.loc[info['item'] == '行业', 'value'].iloc[0]
            list_date = info.loc[info['item'] == '上市时间', 'value'].iloc[0]
            total_equity = info.loc[info['item'] == '总股本', 'value'].iloc[0]
            flow_equity = info.loc[info['item'] == '流通股', 'value'].iloc[0]
            total_cap = info.loc[info['item'] == '总市值', 'value'].iloc[0]
            flow_cap = info.loc[info['item'] == '流通市值', 'value'].iloc[0]

            basic_dao.add(code, row['名称'], industry, list_date, total_equity, flow_equity, total_cap, flow_cap)
        except Exception as e:
            print(basic, info)
            traceback.print_exc()
    else:
        days = date_util.date_diff(basic.list_date, now())
        if days <= 30:
            basic_dao.update(code, row['名称'], row['总市值'], row['流通市值'])
            print(code, 'update basic name', row['名称'])

