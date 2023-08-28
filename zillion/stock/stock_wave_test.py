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
        wave_daily_df = stock_us_daily_df[stock_us_daily_df['date'] > '2022-01-01']
        wave_df = wave.get_wave(code, hist_data=wave_daily_df, begin_low=True, duration=0, change=0)
        if wave_df is not None and size >= 1:
            wave_str = wave.wave_to_str(wave_df)
            wave_list = wave.get_wave_list(wave_str)
            wave_detail_list.append(wave_df)
            wave_list.append(wave_df.tail(1).iloc[0, 5])  # end_price
            wave_list.insert(0, code)
            # wave_list.insert(1, code.split('.')[0])
            wave_list.insert(1, list(wave_df['begin'])[0])
            wave_list.insert(2, list(wave_df['end'])[-1])
            wave_data_list.append(wave_list)
        else:
            print(code, wave_df)
        print(code, size)
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
    df_data = db_stock.read_sql('select code from basic_us_selected order by id', params={})
    codes = list(df_data['code'])
    # codes = ['LIN']
    do_wave(codes)
