import pandas as pd
import tushare as ts

from stocks.data import data_util
from stocks.util import date_util
from stocks.util import db_util
from stocks.util.db_util import get_db


def update_latest_limit_up_stat():
    '''
    实时指定日期涨停信息
    :return:
    '''
    latest_trade_date = date_util.get_latest_trade_date(1)[0]
    target_date = date_util.get_previous_trade_day(latest_trade_date)
    print(target_date, 'Update limit up stat start ...')
    limit_up_stat_df = get_limit_up_stat(start=target_date, end=target_date)
    if limit_up_stat_df is not None:
        # 建立数据库连接
        db = get_db()
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        codes = set(limit_up_stat_df['code'])
        if len(codes) == 0:
            print('>>> failed', target_date, 'no limit up stat found')
        else:
            realtime_df = ts.get_realtime_quotes(codes)
            index_df = ts.get_index()
            index_df.index = index_df['code']
            for index, row in limit_up_stat_df.iterrows():
                row_trade_date = row['trade_date']
                code = row['code']
                try:
                    next_low_than_open = 0
                    next_open_change = 0
                    next_open_buy_change = 0
                    next_low_change = 0
                    next_low_buy_change = 0
                    ref_index_change = 0

                    # 下一交易日指数情况
                    # 000001.SH  399001.SZ  399006.SZ
                    if code[:1] == '6':
                        ref_index_change = index_df.loc['000001', 'change']
                    elif code[:1] == '0':
                        ref_index_change = index_df.loc['399001', 'change']
                    elif code[:1] == '3':
                        ref_index_change = index_df.loc['399006', 'change']

                    # 下一交易日实时个股情况
                    next_hist_df = realtime_df[(realtime_df['code'] == code)]
                    if next_hist_df is None or next_hist_df.empty:
                        print('>>> failed', code, 'no trade data found, please check!')
                    else:
                        next_trade_index = next_hist_df.index[0]
                        next_open = float(next_hist_df.loc[next_trade_index, 'open'])
                        next_pre_close = float(next_hist_df.loc[next_trade_index, 'pre_close'])
                        next_low = float(next_hist_df.loc[next_trade_index, 'low'])
                        next_close = float(next_hist_df.loc[next_trade_index, 'price'])

                        next_low_than_open = 1 if next_low < next_open else 0
                        next_open_change = round((next_open - next_pre_close) / next_pre_close * 100, 2)
                        next_low_change = round((next_low - next_pre_close) / next_pre_close * 100, 2)
                        next_open_buy_change = round((next_close - next_open) / next_open * 100, 2)
                        next_low_buy_change = round((next_close - next_low) / next_low * 100, 2)

                    update_time = date_util.now()
                    values = (int(next_low_than_open), float(next_open_change), float(next_open_buy_change),
                              float(next_low_change), float(next_low_buy_change), float(ref_index_change),
                              update_time, row_trade_date, code)
                    update_sql = "update limit_up_stat set next_low_than_open = %s, next_open_change = %s, " \
                                 "next_open_buy_change = %s, next_low_change = %s, next_low_buy_change = %s, ref_index_change = %s, " \
                                 "update_time = %s where trade_date = %s and code = %s"
                    cursor.execute(update_sql, values)
                    db.commit()
                    print(target_date, code, 'Update limit up stat successfully.')
                except Exception as err:
                    print('  >>>error:', err)
                    db.rollback()

    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


def update_limit_up_stat(target_date):
    '''
    更新指定日期涨停信息
    :param target_date: YYYY-MM-DD
    :return:
    '''
    trade_date = date_util.get_latest_trade_date(1)[0]
    if target_date is None or target_date > trade_date:
        target_date = trade_date
    if date_util.is_tradeday(target_date) is False:
        target_date = date_util.get_next_trade_day(target_date)

    while True:
        print(target_date, 'Update limit up stat start ...')
        limit_up_stat_df = get_limit_up_stat(start=target_date, end=target_date)
        if limit_up_stat_df is not None:
            # 建立数据库连接
            db = get_db()
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            codes = set(limit_up_stat_df['code'])
            if len(codes) == 0:
                print('>>> failed', target_date, 'no limit up stat found')
            else:
                hist_data_df = data_util.get_hist_trade(code=codes, start=target_date)
                hist_index_df = data_util.get_hist_trade(start=target_date, is_index=True)
                for index, row in limit_up_stat_df.iterrows():
                    row_trade_date = row['trade_date']
                    code = row['code']
                    try:
                        next_trade_date = date_util.get_next_trade_day(row_trade_date)
                        # 下一个交易日没到，结束
                        if next_trade_date > date_util.get_today():
                            print(trade_date, '已是最近一个交易日，下个交易日结束再执行 end')
                            break

                        next_low_than_open = 0
                        next_open_change = 0
                        next_open_buy_change = 0
                        next_low_change = 0
                        next_low_buy_change = 0
                        ref_index_change = 0

                        # 下一交易日指数情况
                        next_index_df = hist_index_df[(hist_index_df['trade_date'] == next_trade_date)]
                        if next_index_df is None or next_index_df.empty:
                            if index == 0:
                                print('  >>> warn', next_trade_date, 'no index data found, please check!')
                        else:
                            next_index_map = {}
                            for idx, index_row in next_index_df.iterrows():
                                # 000001.SH  399001.SZ  399006.SZ
                                index_code = index_row['code']
                                pct_change = index_row['pct_change']
                                next_index_map[index_code] = pct_change
                            if code[:1] == '6':
                                ref_index_change = next_index_map.get('000001')
                            elif code[:1] == '0':
                                ref_index_change = next_index_map.get('399001')
                            elif code[:1] == '3':
                                ref_index_change = next_index_map.get('399006')

                        # 下一交易日个股情况
                        next_hist_df = hist_data_df[(hist_data_df['trade_date'] == next_trade_date)
                                                    & (hist_data_df['code'] == code)]
                        if next_hist_df is None or next_hist_df.empty:
                            print('  >>> failed', code, next_trade_date, 'no trade data found, please check!')
                        else:
                            next_trade_index = next_hist_df.index[0]
                            next_open = next_hist_df.loc[next_trade_index, 'open']
                            next_pre_close = next_hist_df.loc[next_trade_index, 'pre_close']
                            next_low = next_hist_df.loc[next_trade_index, 'low']
                            next_close = next_hist_df.loc[next_trade_index, 'close']

                            next_low_than_open = 1 if next_low < next_open else 0
                            next_open_change = round((next_open - next_pre_close) / next_pre_close * 100, 2)
                            next_low_change = round((next_low - next_pre_close) / next_pre_close * 100, 2)

                            next_open_buy_change = round((next_close - next_open) / next_open * 100, 2)
                            next_low_buy_change = round((next_close - next_low) / next_low * 100, 2)

                            update_time = date_util.now()
                            values = (int(next_low_than_open), float(next_open_change), float(next_open_buy_change),
                                      float(next_low_change),
                                      float(next_low_buy_change), float(ref_index_change), update_time, row_trade_date,
                                      code)
                            update_sql = "update limit_up_stat set next_low_than_open = %s, next_open_change = %s, " \
                                         "next_open_buy_change = %s, next_low_change = %s, next_low_buy_change = %s, ref_index_change = %s, " \
                                         "update_time = %s where trade_date = %s and code = %s"
                            cursor.execute(update_sql, values)
                            db.commit()
                            # print('  >>>', target_date, code, 'Update limit up stat successfully.')
                    except Exception as err:
                        print('  >>>error:', err)
                        db.rollback()
            # 关闭游标和数据库的连接
            cursor.close()
            db.close()

        next_trade_date = date_util.get_next_trade_day(target_date)
        if next_trade_date > date_util.get_today():
            break
        target_date = next_trade_date

    print(target_date, 'Update limit up stat end ...')


def collect_limit_up_stat(target_date):
    '''
    采集指定日期涨停信息
    :param target_date: YYYY-MM-DD
    :return:
    '''
    trade_date = date_util.get_latest_trade_date(1)[0]
    if target_date is None or target_date > trade_date:
        target_date = trade_date
    if date_util.is_tradeday(target_date) is False:
        target_date = date_util.get_next_trade_day(target_date)
    while True:
        print(target_date, 'Collect limit up stat start ...')
        limit_up_df = data_util.get_hist_trade(start=target_date, end=target_date, is_limit=True)

        if limit_up_df is not None:
            codes = list(limit_up_df['code'])
            limit_up_count = get_limit_up_times(code_list=codes, target_date=target_date)
            limit_up_count_codes = list(limit_up_count['code'])
            insert_values = []
            for index, row in limit_up_df.iterrows():
                code = row['code']
                combo_times = 1
                if code in limit_up_count_codes:
                    index = limit_up_count_codes.index(code)
                    combo_times = limit_up_count.loc[index, 'combo']
                else:
                    print(code, 'limit up not found in hist data, trade date', target_date)

                close_change = round(row['pct_change'], 2)
                open = row['open']
                pre_close = row['pre_close']
                open_change = round((open - pre_close) / pre_close * 100, 2)
                insert_values.append((target_date, code, '', open_change, close_change, int(combo_times)))
            total_size = len(insert_values)
            # 建立数据库连接
            db = get_db()
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            try:
                # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
                insert_count = cursor.executemany(
                    'insert into limit_up_daily(trade_date, code, name, open_change, close_change, combo) '
                    'values(%s, %s, %s, %s, %s, %s)', insert_values)
                cursor.execute("update limit_up_daily l inner join basics b on l.code = b.code set l.name=b.name where l.name=''")
                db.commit()
                print(target_date, 'Collect limit up daily finished! Total size: '
                      + str(total_size) + ' , ' + str(insert_count) + ' insert successfully.')
            except Exception as err:
                print('  >>>error:', err)
                db.rollback()
            # 关闭游标和数据库的连接
            cursor.close()
            db.close()

        next_trade_date = date_util.get_next_trade_day(target_date)
        if next_trade_date > date_util.get_today():
            break
        target_date = next_trade_date


def get_limit_up_times(code_list, target_date=None):
    '''
    获取指定日期连续涨停次数
    :param code_list:
    :param target_date:
    :return: ['trade_date', 'code', 'combo_times']
    '''
    if len(code_list) == 0:
        return None
    if date_util.is_tradeday(target_date) is False:
        target_date = date_util.get_next_trade_day(target_date)
    start_date = date_util.shift_date(type='m', from_date=target_date, n=-1)
    limit_up_trade_data = data_util.get_hist_trade(code=code_list, start=start_date, end=target_date, is_limit=True)

    limit_group_df = limit_up_trade_data.groupby(limit_up_trade_data['code'])
    data_list = []
    for code, group in limit_group_df:
        curt_data = [target_date, code]
        up_limit_dates = list(group['trade_date'])
        total = len(up_limit_dates)
        continue_count = 1
        if total < 2:
            curt_data.append(continue_count)
        else:
            curt_trade_date = up_limit_dates[total - 1]
            for i in range(total):
                pre_trade_date = date_util.get_previous_trade_day(curt_trade_date)
                pre_limit_date = up_limit_dates[total - (i + 2)]
                if pre_trade_date == pre_limit_date:
                    continue_count += 1
                    curt_trade_date = pre_limit_date
                    continue
                curt_data.append(continue_count)
                break
        data_list.append(curt_data)

    result_df = pd.DataFrame(data_list, columns=['trade_date', 'code', 'combo'])
    return result_df


def get_limit_up_stat(code=None, start=None, end=None):
    sql = 'select * from limit_up_stat where 1=1 '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if start is not None:
        sql += 'and trade_date >=:start '
    if end is not None:
        sql += 'and trade_date <=:end '

    params = {'code': code, 'start': start, 'end': end}
    df = db_util.read_sql(sql, params=params)
    return df


if __name__ == '__main__':
    # get_limit_up_times(code_list=['000716', '002105', '600513'], target_date='2020-01-01')
    # collect_limit_up_stat(target_date='2020-02-20')
    # update_limit_up_stat(target_date='2020-02-01')

    collect_limit_up_stat(target_date=date_util.get_this_week_start())
    update_limit_up_stat(target_date=date_util.get_previous_trade_day(date_util.get_this_week_start()))

    # update_latest_limit_up_stat()
