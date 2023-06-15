import akshare
import pandas as pd

from zillion.future.app import wave
from zillion.stock import db_stock
from zillion.utils import date_util
from zillion.utils.date_util import parse_date_str


def do_wave(code_list=['BABA']):
    print(date_util.now_str())
    ############################################################
    # code_list = ['']
    ############################################################
    # code_list = ['FG0']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    size = len(code_list)
    for code in code_list:
        stock_us_daily_df = None
        if stock_us_daily_df is None or stock_us_daily_df.empty is True:
            # df_data = pro.us_daily(ts_code=code')
            stock_us_daily_df = akshare.stock_us_daily(symbol=code, adjust="qfq")
            stock_us_daily_df['date'] = stock_us_daily_df['date'].apply(lambda x: parse_date_str(x))
            db_stock.to_db(stock_us_daily_df, 'trade_daily_us')
        wave_daily_df = stock_us_daily_df[stock_us_daily_df['date'] > '2015-12-31']
        wave_df = wave.get_wave(code, hist_data=wave_daily_df, begin_low=True, duration=0, change=0)
        wave_str = wave.wave_to_str(wave_df)
        wave_list = wave.get_wave_list(wave_str)
        wave_detail_list.append(wave_df)
        wave_list.append(wave_df.tail(1).iloc[0, 5])  # end_price
        wave_list.insert(0, code)
        wave_list.insert(1, code.split('.')[0])
        wave_list.insert(2, list(wave_df['begin'])[0])
        wave_list.insert(3, list(wave_df['end'])[-1])
        wave_data_list.append(wave_list)
        print(size)
        size = size - 1

    wave_to_db(wave_data_list, wave_detail_list)
    print(date_util.now_str())


def wave_to_db(wave_list=None, wave_detail_list=None):
    wave_df_result = pd.DataFrame(wave_list,
                                  columns=['code', 'code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp', 'dp',
                                           'p'])
    wave_df_result['update_time'] = date_util.now()
    db_stock.to_db(wave_df_result, 'wave')
    wave_detail_result = pd.DataFrame(pd.concat(wave_detail_list),
                                      columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price',
                                               'change', 'days'])
    db_stock.to_db(wave_detail_result, 'wave_detail')


if __name__ == '__main__':
    # try:
    #     df_data = db_stock.read_sql(
    #         'select ts_code code, trade_date date, open, high, low, close from trade_daily_us order by trade_date',
    #         params={})
    # except Exception as e:
    #     print(e)
    #     df_data = None
    codes = ["AAPL","MSFT","GOOG","GOOGL","AMZN","NVDA","BRK.A","TSLA","BRK.B","META","TSM","V","UNH","XOM","LLY","JNJ","JPM","WMT","VXUS","NVO","MA","PG","AVGO","HD","CVX","ORCL","ASML","MRK","KO","PEP","ABBV","BAC","COST","AZN","BABA","PFE","NVS","MCD","CRM","CSCO","SHEL","ADBE","TM","TMO","AMD","ACN","RDS.A","FMX","NFLX","LIN","ABT","DHR","DIS","CMCSA","SAP","NKE","WFC","TMUS","TXN","HSBC","BHP","NEE","VZ","VUG","UPS","TTE","TBB","RTX","MS","PM","VO","BMY","INTC","HON","BA","QCOM","SNY","RY","AXP","TOT","COP","UL","LOW","SPGI","UNP","IBM","JJEB","CAT","HDB","SONY","INTU","AMGN","LMT","ANTM","GE","PLD","T","AMAT","SBUX","COWB","JJTB","BALB","DE","VB","GS","JJGB","MDT","ELV","BUD","NOW","ISRG","TD","BNDX","JJAB","BJJN","JJUB","SYK","RIO","BP","JJSB","JJPB","BLK","SGGB","JJMB","SCHW"]
    do_wave(codes)
