import stocks.util.db_util as _dt
from stocks.future import future_util
from stocks.util import date_util


def save_gap(values=None):
    if values is not None and len(values) > 0:
        try:
            # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
            cursor.executemany(
                'insert into gap_log '
                '(code, start_date, end_date, gap_type, start_price, end_price, gap_rate, is_fill, update_time) '
                'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            db.commit()
        except Exception as err:
            print('  >>>error:', err)
        db.rollback()


if __name__ == '__main__':
    ############################################################
    select_main_codes = "select concat(code, '.', exchange) ts_code from future_basic where deleted=0"
    main_codes_df = future_util.select_from_sql(select_main_codes)
    code_list = list(main_codes_df['ts_code'])
    ############################################################
    # code_list = ['AP2205.ZCE']
    ############################################################
    wave_data_list = []
    wave_detail_list = []
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    for code in code_list:
        df_data = future_util.get_ts_future_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
        if df_data is None or df_data.empty:
            print(code + ' no daily data!')
            continue
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        date_list = list(df_data['date'])
        high_list = list(df_data['high'])
        low_list = list(df_data['low'])
        insert_values = []
        for index, row in df_data.iterrows():
            if index == len(high_list) - 1:
                break
            begin_low = low_list[index]
            begin_high = high_list[index]
            lowest = min(low_list[index + 1:])
            highest = max(high_list[index + 1:])
            # 向下跳空缺口
            if begin_low > highest:
                highest_index = high_list.index(highest, index + 1)
                insert_values.append((row['code'].split('.')[0], row['date'], date_list[highest_index], '向下跳空',
                                      begin_low, highest,
                                      round((highest - begin_low) * 100 / begin_low, 2), 0, date_util.now()))
            # 向上跳空缺口
            if begin_high < lowest:
                lowest_index = low_list.index(lowest, index + 1)
                insert_values.append((row['code'].split('.')[0], row['date'], date_list[lowest_index], '向上跳空',
                                      begin_high, lowest,
                                      round((lowest - begin_high) * 100 / begin_high, 2), 0, date_util.now()))

        # to db
        save_gap(insert_values)
    print('done @', date_util.get_now())
