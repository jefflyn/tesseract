import akshare
import numpy as np
import pandas as pd

from utils.datetime import date_util
from utils.datetime.date_util import now_str
from zillion.utils import notify_util
from zillion.utils.position_util import calc_position

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

baba_target_price = 130.0


def custom_function(row):
    return calc_position(float(row['最新价']), float(row['最低价']), float(row['最高价']))


def format_realtime(df):
    """
    格式化数据
    :param df:
    :return:
    """
    df.insert(2, 'pos', np.nan)
    df['pos'] = df.apply(custom_function, axis=1)
    df['涨跌幅'] = df['涨跌幅'].map(str) + '%'
    df['最新价'] = '【' + df['最新价'].map(str) + '】'
    df = df.drop(columns=['序号'])
    realtime_df = df.sort_values(by=['总市值'], ascending=False, ignore_index=True)

    return realtime_df


def hist():
    print(akshare.stock_us_hist())
    print(akshare.stock_us_daily())


def us_realtime_em(code_list=None):
    df = akshare.stock_us_spot_em()
    # print(df)
    # df['time'] = date_util.now_str()
    # db_stock.to_db(df, 'basic_hk')
    if code_list is not None:
        df = df[df['代码'].isin(code_list)]
    # baba_pr = df.loc[df['代码'] == '106.BABA', '最新价'].iloc[0]
    # global baba_target_price
    # if baba_pr > baba_target_price:
    #     notify_util.notify('📣 baba @' + date_util.time_str(), '️🏁🏁🏁', '⬆️' + str(baba_pr))
    #     baba_target_price = baba_pr * 1.01
    if df.empty is True:
        return
    return format_realtime(df)


if __name__ == '__main__':
    print(us_realtime_em(['105.AAPL', '105.MSFT', '105.GOOG', '105.AMZN', '105.NVDA', '105.META', '105.TSLA',
                          '106.BABA', '105.PDD', '105.JD']))
    print('time:', now_str())
