import tushare as ts
import pandas as pd
from stocks.util.db_util import get_db
from stocks.util import date_util
from stocks.data import data_util
from stocks.gene import wave


def collect_limit_up_data(target_date):
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
        print('collect_limit_up_data, trade date=', target_date)
        day_all_df = ts.get_day_all(date=target_date)
        # close = round(pre_close * 1.1, 2)
        limit_up_df = day_all_df[(day_all_df['price'] == round(day_all_df['preprice'] * 1.1, 2)) & (day_all_df['p_change'] > 9)]
        codes = list(limit_up_df['code'])
        limit_up_count = get_limit_up_times(code_list=codes, target_date=target_date)
        limit_up_count_codes = list(limit_up_count['code'])
        insert_values = []
        for index, row in limit_up_df.iterrows():
            code = row['code']
            combo_times = 1
            if code in limit_up_count_codes:
                index = limit_up_count_codes.index(code)
                combo_times = limit_up_count.loc[index, 'combo_times']
            else:
                print(code, 'limit up not found in hist data, trade date', target_date)

            wave_ab = wave.get_wave_ab_by_code(code)
            if wave_ab is None:
                continue
            wave_a = round(wave_ab[0], 2)
            wave_b = round(wave_ab[1], 2)
            open = row['open']
            pre_close = row['preprice']
            open_change = round((open - pre_close) / pre_close * 100, 2)
            insert_values.append((target_date, code, row['name'], row['industry'], row['area'], row['pe'],
                                  int(combo_times), float(wave_a), float(wave_b),
                                  row['turnover'], row['volratio'], float(open_change)))
        total_size = len(insert_values)
        # 建立数据库连接
        db = get_db()
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        try:
            # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
            insert_count = cursor.executemany(
                'insert into limit_up_stat(trade_date, code, name, industry, area, pe, combo_times, wave_a, wave_b, '
                'turnover_rate, vol_rate, open_change) '
                'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', insert_values)
            db.commit()
            print(target_date + ': Collect limit up stat finished! Total size: '
                  + str(total_size) + ' , ' + str(insert_count) + ' insert successfully.')
        except Exception as err:
            print('>>>error:', err)
            db.rollback()

        next_trade_date = date_util.get_next_trade_day(target_date)
        if next_trade_date > date_util.get_today():
            break
        target_date = next_trade_date

    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


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

    result_df = pd.DataFrame(data_list, columns=['trade_date', 'code', 'combo_times'])
    return result_df


if __name__ == '__main__':
    # get_limit_up_times(code_list=['000716', '002105', '600513'], target_date='2020-01-01')
    collect_limit_up_data(target_date='2019-01-02')



