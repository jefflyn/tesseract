import pandas as pd
import tushare as ts

import stocks.util.db_util as _dt
from stocks.data import data_util


def period_change_stat(code=None, trade_date=None):
    target = ['000001', '000016', '000300', '399001', '399005', '399006']
    index_df = ts.get_index()
    index_df = index_df[index_df['code'].isin(target)]
    index_df.index = list(index_df['code'])
    index_hist_df = data_util.get_hist_trade(code=code, is_index=True, start=trade_date, end=trade_date)
    index_change_map = {}
    for index, row in index_hist_df.iterrows():
        code = row['code']
        low = float(row['low'])
        curt_point = float(index_df.loc[code, 'close'])
        pct_change = (curt_point - low) / low * 100
        index_change_map[code] = str(round(pct_change, 2)) + '|' + str(round(low, 2))

    stock_hist_df = data_util.get_hist_trade(start=trade_date, end=trade_date)
    data_list = []
    for index, row in stock_hist_df.iterrows():
        print(index)
        code = row['code']
        stock_df = ts.get_realtime_quotes(code)
        if stock_df is None or stock_df.empty:
            continue
        stock_df.index = [code]
        curt_price = float(stock_df.loc[code, 'price'])
        name = stock_df.loc[code, 'name']
        low = float(row['low'])
        pct_change = round((curt_price - low) / low * 100, 2)

        curt_data = [code, name, trade_date, round(low, 2), pct_change,
                     index_change_map['000001'], index_change_map['399001'], index_change_map['399006'],
                     index_change_map['000016'], index_change_map['000300'], index_change_map['399005'],
                     ]
        data_list.append(curt_data)

    result_df = pd.DataFrame(data_list, columns=['code', 'name', 'from_date', 'low_price', 'period_change',
                                                 'hz_change', 'sz_change', 'cy_change',
                                                 '50_change', '300_change', 'zx_change', ])
    print(result_df.head(10))
    _dt.to_db(result_df, 'period_change')


if __name__ == '__main__':
    period_change_stat(code=None, trade_date='2020-03-19')
