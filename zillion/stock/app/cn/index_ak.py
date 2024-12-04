# coding: utf-8
import akshare as ak
import pandas as pd

from utils.datetime.date_util import now_str
from zillion.utils.price_util import format_large_number

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


TAR_IDX_CODES = ['sh000001', 'sh000016', 'sz399001', 'sz399005', 'sz399006']


def format_index(df):
    """
    格式化数据
    :param df:
    :return:
    """
    df['涨跌幅'] = df['涨跌幅'].apply(lambda x: str(round(x, 2)) + '%')
    df['成交额'] = df['成交额'].apply(lambda x: str(format_large_number(x)))

    return df


def get_quote():
    index_df = ak.stock_zh_index_spot_sina()
    filtered_df = index_df[index_df['代码'].isin(TAR_IDX_CODES)]
    # filtered_df['成交额'] = format_large_number_vectorized(filtered_df['成交额'])
    return format_index(filtered_df)


if __name__ == '__main__':
    print(get_quote())
    print('quote time:', now_str())


