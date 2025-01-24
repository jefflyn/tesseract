import akshare as ak

from utils.datetime import date_util
from zillion.db.DataSourceFactory import session_stock
from zillion.stock.dao.basic_a_dao import BasicADAO


def hist_a():
    '''
    历史行情数据 https://akshare.akfamily.xyz/data/stock/stock.html#id21
    :return:
    '''
    # 东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20241007", end_date='20241008',
                                            adjust="qfq")
    print(stock_zh_a_hist_df)
    # return stock_zh_a_hist_df

def get_hist_data(symbol, start_date, end_date):
    return ak.stock_zh_a_hist(symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")


def collect_all_hist_data():
    basic_dao = BasicADAO(session_stock)
    all = basic_dao.get_all()
    size = len(all)
    last_trade_date = date_util.get_today(date_util.FORMAT_FLAT)
    start = 1
    for basic in all:
        code = basic.code
        df = get_hist_data(code, '20190101', last_trade_date)
        df.to_csv("hist_a.csv", mode='a', index=False, header=False, encoding="utf-8")
        print(str(start) + '/' + str(size) + ' ' + code)
        start += 1

if __name__ == '__main__':
    collect_all_hist_data()