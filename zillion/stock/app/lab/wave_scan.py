import numpy as np
import pandas as pd

from zillion.stock.data import data_util as _dt
from zillion.utils import db_util


def scan_wave_change(wave_data=None, tb_name='wave_change_ref'):
    """
    scan wave data info
    :param wave_data:
    :param tb_name:
    :return:
    """
    all_wave_data = wave_data
    wave_group = all_wave_data.groupby('code')
    wave_map = dict()
    wave_up_total = 0
    wave_down_total = 0
    count = 0
    for code, group in wave_group:
        count += 1
        print(str(count) + ':' + code)
        # 重置index
        group = group.reset_index(drop=True)
        index_list = group.index.to_numpy()
        first_row = index_list[0]
        last_row = index_list[-1]
        # 去掉头尾行
        group.drop(group.index[[first_row, last_row]], inplace=True)
        size = len(index_list) - 2

        for index in index_list[first_row + 1:last_row - 1]:
            pre_data = group.ix[index]
            nxt_data = group.ix[index + 1]
            pre_change = pre_data['change']
            nxt_change = nxt_data['change']
            # 只考虑涨跌幅20的波段
            if abs(pre_change) < 20 or abs(nxt_change) < 20:
                continue
            wave_pair = (pre_change, nxt_change)
            wave_map_key = round(pre_change, -1)
            wave_list = wave_map.get(wave_map_key)
            if wave_list is None:
                wave_list = list()
            wave_list.append(wave_pair)
            wave_map[wave_map_key] = wave_list
            if wave_map_key > 0:
                wave_up_total += 1
            else:
                wave_down_total += 1
    wave_result_list = []
    for key, value in wave_map.items():
        avg_change = np.min([v[0] for v in value])
        min_change = np.min([v[1] for v in value])
        mean_change = np.mean([v[1] for v in value])
        max_change = np.max([v[1] for v in value])
        if key > 0:
            ratio = round(len(value) / wave_up_total * 100, 2)
            wave_result_data = [key, avg_change, len(value), ratio, round(mean_change, 2), max_change, min_change]
        else:
            ratio = round(len(value) / wave_down_total * 100, 2)
            wave_result_data = [key, avg_change, len(value), ratio, round(mean_change, 2), min_change, max_change]
        wave_result_list.append(wave_result_data)

    wave_change_df = pd.DataFrame(wave_result_list, columns=['range', 'avg_range', 'count', 'ratio', 'avg_change',
                                                             'min_change', 'max_change'])
    wave_change_df = wave_change_df.sort_values("range", axis=0, ascending=True, inplace=False, kind='quicksort',
                                                na_position='last')
    db_util.to_db(wave_change_df, tb_name)
    print(wave_map)


if __name__ == '__main__':
    scan_wave_change(_dt.get_normal_wave_data(), 'wave_change_normal_ref')
    # scan_wave_change(_dt.get_subnew_wave_data(), 'wave_change_subnew_ref')
    # scan_wave_change(_dt.get_st_wave_data(), 'wave_change_st_ref')

