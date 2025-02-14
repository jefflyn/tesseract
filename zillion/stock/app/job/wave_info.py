import zillion.stock.app.cn.service.hist_trade_service as hts
from utils.datetime import date_util
from zillion.stock.data import data_util
from zillion.stock.gene import wave
from zillion.utils.db_util import get_db

# 建立数据库连接
db = get_db()
cursor = db.cursor()


def get_wave_info(codes=[]):
    """
    """
    basics = data_util.get_basics()
    open_date_map = hts.get_new_open_date()
    size = len(codes)
    for code in codes:
        size = size - 1
        fundamental = basics[basics.code == code]
        if fundamental is None:
            print(code, ' no basics info found')
            continue
        # list_date = fundamental.loc[code, 'list_date']
        try:
            open_date = open_date_map[code]
            wave_df = wave.get_wave(code, is_index=False, start=open_date, pchange=20)
        except Exception:
            print(code, "not open yet! continue...")
            continue
        print(str(size), code, ' get wave from ', open_date)
        wave_str = wave.wave_to_str(wave_df, size=100)
        print(wave_str)
        wave_list = wave_str.split('\n')[0].split('|')
        day_list = wave_str.split('\n')[1].split('|')
        # print(day_list)
        wa = 0
        wb = 0
        wc = 0
        d1 = 0
        d2 = 0
        d3 = 0
        for i in range(1, len(wave_list)):
            if i == 1:
                wa = float(wave_list[i])
                d1 = int(day_list[i])
            elif i == 2:
                wb = float(wave_list[i])
                d2 = int(day_list[i])
            else:
                wc = wc + float(wave_list[i])
                d3 = d3 + int(day_list[i])
        try:
            cursor.execute("delete from wave_info where code='" + code + "'")
            sql_insert = "INSERT INTO wave_info(code, from_date, to_date, wave_a, wave_b, wave_c, adays, bdays, cdays, " \
                         "update_time) " \
                         "VALUES ('%s', '%s', '%s', '%.2f', '%.2f','%.2f','%i','%i','%i','%s')" \
                         % (code, open_date, date_util.get_today(), wa, wb, wc, d1, d2, d3, date_util.now_str())
            cursor.execute(sql_insert)
            db.commit()
        except Exception as err:
            print('>>> insert data failed!', err)
            db.rollback()


if __name__ == '__main__':
    sql = "select code from basics where code not like '688%' and list_date between 20200101 and 20210101"
    stock_pool = data_util.get_codes_from_sql(sql)
    if len(stock_pool) == 0:
        print("no stock found, process end!")
        exit(0)
    # stock_pool = ['300789']
    get_wave_info(stock_pool)


