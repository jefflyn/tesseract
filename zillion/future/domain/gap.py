import zillion.future.db_util as _dt
from zillion.future.app import wave
from zillion.future.domain import daily
from zillion.utils import date_util

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def save_gap(values=None):
    if values is not None and len(values) > 0:
        try:
            # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
            cursor.executemany(
                'insert into gap_log '
                '(ts_code, code, start_date, end_date, gap_type, start_price, cpos, end_price, gap_rate, is_fill, create_time, update_time) '
                'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            db.commit()
        except Exception as err:
            print('  >>> insert gap log error:', err)


def update_gap_record(end_price, end_date, code, start_date):
    sql = "update gap_log set end_price=%d, end_date='%s', is_fill=1, fill_date='%s', " \
          "update_time=now() where code='%s' and start_date='%s';"
    cursor.execute(sql % (end_price, end_date, date_util.parse_date_str(end_date), code, start_date))
    db.commit()


def del_gap_record(code):
    sql = "delete from gap_log where code='%s';"
    cursor.execute(sql % code)
    db.commit()
    print("Delete gap record ", code)


def update_gap():
    gap_df = _dt.read_sql('select * from gap_log where is_fill=0', params=None)
    for index, row in gap_df.iterrows():
        code = row['code']
        start_date = row['start_date']
        gap_price = row['start_price']
        type = row['gap_type']
        # basic = codes_df[codes_df.code == code]
        print(code, 'update gap...')
        # if basic.empty is True:
        #     print(code, 'contract changed!')
        #     # del_gap_record(code)
        #     continue
        # ts_code = basic.loc[basic.index.to_numpy()[0], 'main_code']
        daily_df = daily.get_daily(code, start_date=start_date)[
            ['code', 'trade_date', 'open', 'high', 'low', 'close']]
        if daily_df is None or daily_df.empty:
            print(code + ' no ts daily data!')
            continue
        daily_df.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        date_list = list(daily_df['date'])
        high_list = list(daily_df['high'])
        low_list = list(daily_df['low'])

        lowest = min(low_list[1:])
        highest = max(high_list[1:])
        if type == '跳空高开':
            if lowest <= gap_price:
                lowest_index = low_list.index(lowest, 1)
                update_gap_record(lowest, date_list[lowest_index], code, start_date)
        else:
            if highest >= gap_price:
                highest_index = high_list.index(highest, 1)
                update_gap_record(highest, date_list[highest_index], code, start_date)


def add_gap(code_list):
    ############################################################
    # code_list = ['AL.SHF']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    high_low_df = wave.get_high_low()
    size = len(code_list)
    curt_date = date_util.get_today()
    for code in code_list:
        print(size)
        size -= 1
        start_date = date_util.get_date_before(days=300)
        df_data = daily.get_daily(code, start_date=start_date)
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        df_data = df_data[(df_data['deal_vol'] > 0) | (df_data['trade_date'] == curt_date)]
        df_data = df_data.reset_index()
        df_data = df_data[['code', 'trade_date', 'open', 'high', 'low', 'close']]
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        date_list = list(df_data['date'])
        high_list = list(df_data['high'])
        low_list = list(df_data['low'])
        hl_df = high_low_df[high_low_df.code == code]
        c_low = hl_df.loc[code, 'low']
        c_high = hl_df.loc[code, 'high']
        for index, row in df_data.iterrows():
            if index == len(high_list) - 1:
                break
            begin_low = low_list[index]
            begin_high = high_list[index]
            # next_low = min(low_list[index + 1:])  # 后面所有的最低
            # next_high = max(high_list[index + 1:])  # 后面所有的最高
            next_low = low_list[index + 1]  # 下一日的最低
            next_high = high_list[index + 1]  # 下一日的最高
            # 跳空低开缺口
            if begin_low > next_high:
                highest_index = high_list.index(next_high, index + 1)
                c_pos = round((begin_low - c_low) * 100 / (c_high - c_low), 1)
                save_gap([(row['code'], row['code'].split('.')[0], row['date'], date_list[highest_index], '跳空低开',
                           begin_low, c_pos, next_high,
                           round((next_high - begin_low) * 100 / begin_low, 2), 0, date_util.now(), date_util.now())])
            # 跳空高开缺口
            if begin_high < next_low:
                lowest_index = low_list.index(next_low, index + 1)
                c_pos = round((begin_high - c_low) * 100 / (c_high - c_low), 1)
                save_gap([(row['code'], row['code'].split('.')[0], row['date'], date_list[lowest_index], '跳空高开',
                           begin_high, c_pos, next_low,
                           round((next_low - begin_high) * 100 / begin_high, 2), 0, date_util.now(), date_util.now())])


if __name__ == '__main__':
    txt1 = 'aaa'
    txt2 = 'bbb'
    txt3 = "378.8 @ 201222\n714.4 @ 220609"

    print(txt3)
    # print('done @', date_util.now_str())
