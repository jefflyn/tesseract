import pandas as pd

import zillion.utils.db_util as _dt
from zillion.future import future_util
from zillion.utils import date_util
from zillion.utils.date_util import FORMAT_FLAT

monthly_contract = [
    # 'AL.SHF', 'BC.INE', 'CU.SHF', 'LU.INE', 'NI.SHF',
    # 'PB.SHF', 'PG.DCE', 'SC.INE', 'SN.SHF', 'SS.SHF',
    # 'ZN.SHF', 'EB.DCE', 'NR.INE'
]


def in_monthly_contract(code):
    for c in monthly_contract:
        if c.startswith(code):
            return True
    return False


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
    print("delete gap record ", code)


def update_gap(codes_df):
    gap_df = _dt.read_sql('select * from gap_log where is_fill=0', params=None)
    for index, row in gap_df.iterrows():
        code = row['code']
        ts_code = row['ts_code']
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
        ts_daily_df = future_util.get_ts_future_daily(ts_code, start_date=start_date)[
            ['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
        if ts_daily_df is None or ts_daily_df.empty:
            print(code + ' no ts daily data!')
            continue
        ts_daily_df.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        date_list = list(ts_daily_df['date'])
        high_list = list(ts_daily_df['high'])
        low_list = list(ts_daily_df['low'])

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


def add_gap(codes_df_p):
    code_list = list(codes_df_p['ts_code'])
    main_code = list(codes_df_p['main_code'])
    ############################################################
    # code_list = ['AL.SHF']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    size = len(code_list)
    for code in code_list:
        print(size)
        size -= 1
        # 跨月
        if code in monthly_contract:
            start_date = date_util.get_last_2month_start(FORMAT_FLAT)
            df_data = future_util.get_ts_future_daily(code, start_date=start_date)[['ts_code', 'trade_date', 'open',
                                                                                    'high', 'low', 'close']]
            local_last_trade_date = list(df_data['trade_date'])[-1]
            realtime = future_util.add_realtime_data([main_code[code_list.index(code)]], local_last_trade_date)
            if realtime is not None:
                realtime['ts_code'] = code
                realtime.drop(['code', 'date'], axis=1, inplace=True)
                df_data = pd.concat([df_data, realtime], ignore_index=True)
        else:
            start_date = date_util.get_date_before(days=300, format=FORMAT_FLAT)
            df_data = future_util.get_ts_future_daily(code, start_date=start_date)[['ts_code', 'trade_date', 'open',
                                                                                    'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        date_list = list(df_data['date'])
        high_list = list(df_data['high'])
        low_list = list(df_data['low'])
        basic = codes_df[codes_df.ts_code == code]
        c_low = basic.loc[basic.index.to_numpy()[0], 'low']
        c_high = basic.loc[basic.index.to_numpy()[0], 'high']
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
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    sql = "select code, concat(code, '.', exchange) ts_code, " \
          " concat(code, '.', exchange)  main_code, low, high from future_basic where deleted=0;"
    codes_df = _dt.read_sql(sql, params=None)
    # 先更新gap信息
    update_gap(codes_df)

    # 插入新的gap
    add_gap(codes_df)

    print('done @', date_util.get_now())
