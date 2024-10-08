import akshare as ak
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def info_a():
    '''
    个股信息查询 https://akshare.akfamily.xyz/data/stock/stock.html#id8
    :return:
    '''

    # 东方财富-个股-股票信息
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="301618")
    print(stock_individual_info_em_df)


def realtime_a():
    '''
    实时行情数据 https://akshare.akfamily.xyz/data/stock/stock.html#id10
    :return:
    '''
    # 沪深京 A 股-实时行情数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)

    # 沪 A 股-实时行情数据
    stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
    print(stock_sh_a_spot_em_df)

    # 深 A 股-实时行情数据
    stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()
    print(stock_sz_a_spot_em_df)

    # 京 A 股-实时行情数据
    stock_bj_a_spot_em_df = ak.stock_bj_a_spot_em()
    print(stock_bj_a_spot_em_df)


def hist_a():
    '''
    历史行情数据 https://akshare.akfamily.xyz/data/stock/stock.html#id21
    :return:
    '''
    # 东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20240528',
                                            adjust="")
    print(stock_zh_a_hist_df)


def limit():
    '''
    涨停股池
    :return:
    '''

    # 涨停股池（30天）
    stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20240906')
    print(stock_zt_pool_em_df)


def realtime_hk():
    '''
    https://akshare.akfamily.xyz/data/stock/stock.html#id61
    :return:
    '''
    # 东财所有港股的实时行情数据; 该数据有 15 分钟延时
    stock_hk_spot_em_df = ak.stock_hk_spot_em()
    print(stock_hk_spot_em_df)


def realtime_us():
    '''
    https://akshare.akfamily.xyz/data/stock/stock.html#id53
    :return: 
    '''
    # 东财单次返回美股所有上市公司的实时行情数据
    stock_us_daily_df = ak.stock_us_daily(symbol="BABA", adjust="qfq")
    print(stock_us_daily_df)


if __name__ == "__main__":
    info_a()

