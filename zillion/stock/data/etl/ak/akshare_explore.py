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
    df = ak.stock_individual_info_em(symbol="301618")
    print(df.values)


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
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="19910403", end_date='20241008',
                                            adjust="qfq")
    print(stock_zh_a_hist_df)


def index_realtime_a():
    '''
    实时指数数据 https://akshare.akfamily.xyz/data/index/index.html#id1
    :return:
    '''
    # 东方财富网-行情中心-沪深京指数
    stock_zh_index_spot_em_df = ak.stock_zh_index_spot_em(symbol="上证系列指数")
    print(stock_zh_index_spot_em_df)

    # 新浪财经-中国股票指数数据
    stock_zh_index_spot_sina_df = ak.stock_zh_index_spot_sina()
    print(stock_zh_index_spot_sina_df)


def index_hist_a():
    '''
    指数历史数据 https://akshare.akfamily.xyz/data/index/index.html#id3
    :return:
    '''
    # 历史行情数据-新浪
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
    print(stock_zh_index_daily_df)

    # 历史行情数据-东方财富
    stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sz399812")
    print(stock_zh_index_daily_em_df)

    # 东方财富网-中国股票指数-行情数据
    index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000016", period="daily", start_date="19700101", end_date="22220101")
    print(index_zh_a_hist_df)


def limit_a():
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
    index_hist_a()

