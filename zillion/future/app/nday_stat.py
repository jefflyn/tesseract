import pandas as pd

from zillion.future import future_util
from zillion.utils import date_util, db_util


def get_n(change_list):
    up_flag_list = []
    n_list = []

    size = len(change_list)
    for days in range(0, 3, 1):
        # print('day', days)
        if len(n_list) > 0 and max(n_list) > size / 2:
            # print(max(n_list))
            break
        n_list.append(1)
        up_flag = True
        if change_list[days] < 0:
            up_flag = False
        up_flag_list.append(up_flag)

        for n in range(days + 1, size, 1):
            # print('n', n)
            if change_list[n] >= 0 and up_flag:
                n_list[days] += 1
            elif change_list[n] < 0 and up_flag is False:
                n_list[days] += 1
            else:
                break
    print(change_list, up_flag_list, n_list, up_flag_list[n_list.index(max(n_list))], max(n_list))
    return [up_flag_list[n_list.index(max(n_list))], max(n_list)]


if __name__ == '__main__':
    future_basics = future_util.get_future_basics()
    week_end = date_util.get_today(date_util.FORMAT_FLAT)
    week_start = date_util.shift_date_flat_format(n=-30)

    ts_codes = list(future_basics['ts_code'])
    df_data = future_util.get_ts_future_daily(ts_codes, start_date=week_start, end_date=week_end)[
        ['ts_code', 'trade_date', 'pre_close', 'pre_settle', 'open', 'high', 'low', 'close', 'close_change']]

    stat_data = []
    data_group = df_data.groupby('ts_code')
    result = []
    for ts_code, group in data_group:
        last7_data = group.tail(7)
        last7_data = last7_data.sort_values(['trade_date'], ascending=False, ignore_index=True)
        # n_close = 0
        # n = 0
        three_days_change = 0
        five_days_change = 0
        seven_days_change = 0
        last_close = 0
        last_cls_change = 0
        last_settle_change = 0
        close_change_list = []
        for index, row in last7_data.iterrows():
            if index == 0:
                last_close = row['close']
                last_cls_change = round((last_close - row['pre_close']) * 100 / row['pre_close'], 2)
                last_settle_change = round((last_close - row['pre_settle']) * 100 / row['pre_settle'], 2)
            elif index == 2:
                close_change_list.append(round((last_close - row['close']) * 100 / row['close'], 2))
            elif index == 4:
                close_change_list.append(round((last_close - row['close']) * 100 / row['close'], 2))
            elif index == 6:
                close_change_list.append(round((last_close - row['close']) * 100 / row['close'], 2))

            close_change = row['close'] - row['pre_close']
            settle_change = row['close'] - row['pre_settle']

            # if index == 0:
            #     if close_change > 0:
            #         n_close += 1
            #     else:
            #         n_close -= 1
            # else:
            #     if close_change > 0 and n_close > 0 and n == index-1:
            #         n_close += 1
            #         n = index
            #     elif close_change < 0 and n_close < 0 and n == index-1:
            #         n_close -= 1
            #         n = index
        last_cls_change_list = list(last7_data['close_change'])
        n_list = get_n(last_cls_change_list)
        result.append([ts_code, last_cls_change, last_settle_change] + n_list + close_change_list
                      + [str(last_cls_change_list)])

    df = pd.DataFrame(result, columns=['ts_code', 'close_change', 'settle_change', 'up', 'days', '3d_change',
                                       '5d_change', '7d_change', 'change_list'])
    df['update_time'] = date_util.now()
    db_util.to_db(df, 'n_stat', if_exists='replace')
