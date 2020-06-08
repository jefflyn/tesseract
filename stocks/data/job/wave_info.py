from stocks.data import data_util
from stocks.gene import wave
from stocks.util import date_util
from stocks.util.db_util import get_db

# 建立数据库连接
db = get_db()
cursor = db.cursor()


def get_wave_info(codes=[]):
    """
    """
    basics = data_util.get_basics()
    for code in codes:
        fundamental = basics[basics.code == code]
        if fundamental is None:
            print(code, ' no basics info found')
            continue
        list_date = fundamental.loc[code, 'list_date']
        from_date = date_util.parse_date_str(str(list_date), date_util.FORMAT_DEFAULT)
        wave_df = wave.get_wave(code, is_index=False, start=from_date)
        print(code, ' get wave from ', from_date)
        wave_str = wave.wave_to_str(wave_df)
        wave_list = wave_str.split('\n')[0].split('|')
        # print(wave_list)
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
                         % (code, from_date, date_util.get_today(), wa, wb, wc, d1, d2, d3, date_util.get_now())
            cursor.execute(sql_insert)
            db.commit()
        except Exception as err:
            print('>>> insert data failed!', err)
            db.rollback()


if __name__ == '__main__':
    get_code_sql = 'select code from basics where list_date between 20190101 and 20200101'
    total = cursor.execute(get_code_sql)
    if total == 0:
        print("no stock found, process end!")
        exit(0)
    stock_pool = [ts_code_tuple[0] for ts_code_tuple in cursor.fetchall()]
    get_wave_info(stock_pool)


