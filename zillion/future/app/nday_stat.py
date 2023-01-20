import statistics

import pandas as pd

from zillion.future.domain import contract, daily
from zillion.utils import date_util, db_util


def get_n(change_list):
    '''
    compare close with pre-settle, close greater than pre-settle
    :param change_list:
    :return:
    '''
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
    n_day = 14
    codes = list(contract.get_local_contract()['code'])
    week_end = date_util.get_today()
    week_start = date_util.shift_date_flat_format(n=-90)

    df_data = daily.get_daily(codes, start_date=week_start)[
        ['code', 'trade_date', 'pre_close', 'pre_settle', 'open', 'high', 'low', 'close', 'close_change']]

    stat_data = []
    data_group = df_data.groupby('code')
    result = []
    for ts_code, group in data_group:
        last60d_data = group.tail(60)
        last60d_close = list(last60d_data['close'])
        # print(last60d_close)
        size = len(last60d_close)
        price = last60d_close[size-1:][0]
        avg5d = statistics.mean(last60d_close[size-5:])  # attack
        avg10d = statistics.mean(last60d_close[size-10:])  # strategy
        avg20d = statistics.mean(last60d_close[size-20:])  # assist
        avg60d = statistics.mean(last60d_close)  # trend
        print(ts_code, price, avg5d, avg10d, avg20d, avg60d)

        last_n_data = group.tail(n_day)
        last_n_data = last_n_data.sort_values(['trade_date'], ascending=False, ignore_index=True)
        last_n_data['close_diff'] = last_n_data['close'] - last_n_data['pre_close']
        # n_close = 0
        # n = 0
        three_days_change = 0
        five_days_change = 0
        seven_days_change = 0
        last_close = 0
        last_cls_change = 0
        last_settle_change = 0
        close_change_list = []
        for index, row in last_n_data.iterrows():
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

        last_cls_change_list = list(last_n_data['close_diff'])
        n_list = get_n(last_cls_change_list)
        result.append([ts_code, last_cls_change, last_settle_change] + n_list + close_change_list
                      + [str(last_cls_change_list)]
                      + [round(price), round(avg5d), round(avg10d), round(avg20d), round(avg60d)])

    df = pd.DataFrame(result, columns=['code', 'close_change', 'settle_change', 'up', 'days', '3d_change',
                                       '5d_change', '7d_change', 'change_list',
                                       'price', 'avg5d', 'avg10d', 'avg20d', 'avg60d'])
    df['update_time'] = date_util.now()
    db_util.to_db(df, 'n_stat', if_exists='replace')
