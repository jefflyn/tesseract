import zillion.utils.db_util as _dt
from utils.datetime import date_util
from zillion.future.app import wave
from zillion.future.domain import daily
from zillion.utils.price_util import future_price

# 建立数据库连接
db = _dt.get_db("future")
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
    sql = "delete from open_gap_log where code='%s';"
    cursor.execute(sql % code)
    db.commit()
    print("Delete gap record ", code)


def update_gap():
    gap_df = _dt.read_sql('future', 'select * from gap_log where is_fill=0', params=None)
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
        if hl_df is None or hl_df.empty:
            print(high_low_df)
            continue
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
                           future_price(begin_low), c_pos, future_price(next_high),
                           round((next_high - begin_low) * 100 / begin_low, 2), 0, date_util.now(), date_util.now())])
            # 跳空高开缺口
            if begin_high < next_low:
                lowest_index = low_list.index(next_low, index + 1)
                c_pos = round((begin_high - c_low) * 100 / (c_high - c_low), 1)
                save_gap([(row['code'], row['code'].split('.')[0], row['date'], date_list[lowest_index], '跳空高开',
                           future_price(begin_high), c_pos, future_price(next_low),
                           round((next_low - begin_high) * 100 / begin_high, 2), 0, date_util.now(), date_util.now())])



# 计算每天仍然存在的缺口
def find_existing_gaps(data):
    gaps = []
    latest = data.tail(1)
    idx = latest.index.to_numpy()[0]
    latest_price = round(latest.at[idx, 'close'], 2)
    latest_date = latest.at[idx, 'trade_date']
    high_list = list(data['high'])
    low_list = list(data['low'])
    date_list = list(data['trade_date'])
    for index, row in data.iterrows():
        if index == len(high_list) - 1:
            break
        current_date = row['trade_date']
        current_low = round(low_list[index], 2)
        current_high = round(high_list[index], 2)
        # 寻找之后数据中的最高价和最低价
        # next_low = min(low_list[index + 1:])
        # next_high = max(high_list[index + 1:])
        direction = None
        gap_from = None
        gap_to = None
        gap_size = None
        is_closed = 0
        closed_date = None
        days = 0
        current_price = latest_price
        for nxt_idx in range(index + 1, len(high_list)):
            # 下一日
            next_low = round(low_list[nxt_idx], 2)
            next_high = round(high_list[nxt_idx], 2)
            # 忽略当天回补的
            if direction is None and next_low > current_high:
                direction = "向上"
                gap_from = current_high
                gap_to = next_low if gap_to is None or next_low < gap_to else gap_to
                gap_size = round((next_low - current_high) * 100 / current_high, 2)
                current_gap_size = round((current_high - latest_price) * 100 / latest_price, 2)
                days = date_util.date_diff(current_date, latest_date)
            elif direction is None and next_high < current_low:
                direction = "向下"
                gap_from = current_low
                gap_to = next_high if gap_to is None or next_high > gap_to else gap_to
                gap_size = round((next_high - current_low) * 100 / current_low, 2)
                current_gap_size = round((current_low - latest_price) * 100 / latest_price, 2)
                days = date_util.date_diff(current_date, latest_date)
            if direction is None:
                break
            if (direction == "向上" and next_low <= current_high) \
                    or (direction == "向下" and next_high >= current_low):
                is_closed = 1
                closed_date = date_list[nxt_idx]
                days = date_util.date_diff(current_date, closed_date)
                current_gap_size = 0
                break

        # if direction is not None:
            # [(row['code'], current_date, row['close'], row['settle'], row['low'], row['high'], row['open'],
            # open_change,gap_type,gap_rate,contract_pos,
            # is_closed, closed_date, buy_low,sell_high,suggest,suggest_price,checked,create_time,update_time)]
            # data_to_insert = [(row['code'], current_date, pre_close, pre_settle, pre_low,pre_high,
            # open,open_change,gap_type,gap_rate,contract_pos,
            # is_closed, closed_date, buy_low,sell_high,suggest,suggest_price,checked,create_time,update_time)]
            #
            #     [(row['code'], current_date, direction, round(gap_from, 2), round(gap_to, 2), gap_size,
            #                    is_closed, closed_date, days, float(current_price), float(current_gap_size))]
            # print(data_to_insert)

    return gaps



if __name__ == '__main__':
    trade_data = daily.get_daily('SA2405')
    trade_data = trade_data.reset_index()

    find_existing_gaps(trade_data)

    txt1 = 'aaa'
    txt2 = 'bbb'
    txt3 = "378.8 @ 201222\n714.4 @ 220609"

    print(txt3)
    # print('done @', date_util.now_str())
    # add_gap(['BU2406'])