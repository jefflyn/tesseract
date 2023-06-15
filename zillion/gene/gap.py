from datetime import datetime as dtime

import numpy as np
import pandas as pd

from zillion.future import db_util
from zillion.stock.data import data_util
from zillion.utils import _utils
from zillion.utils import date_util

start_date = date_util.DATE_BEFORE_90_DAYS

stock_pool = data_util.get_normal_codes()


def cal_gap(codes=None, seq='W'):
    """
    缺口
    :param codes:
    :param seq:
    :return:
    """
    starttime = dtime.now()
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    hist_data = data_util.get_weekly(code=code_list, start=start_date)

    upndata = []
    for code in code_list:
        histndf = hist_data[hist_data.code == code]
        if histndf is None or len(histndf) < 5:
            continue
        latest = histndf.tail(1)
        idx = latest.index.to_numpy()[0]
        latest_date_str = latest.at[idx, 'trade_date']
        # excluding halting
        if _utils.is_halting(code, latest_date_str):
            continue
        current_price = histndf.loc[idx, 'close']
        histndf = histndf.sort_values('trade_date', ascending=False)
        volumes = [row[1]['vol'] for row in histndf.iterrows()]
        week_vol = []
        n_vol = 5
        for i in range(n_vol):
            sub_vol = volumes[i + 1:i + 1 + n_vol]
            week_vol.append(volumes[i] / np.mean(sub_vol))
        max_v = np.max(week_vol[:2])
        min_v = np.min(week_vol[2:n_vol])
        multi_vol_rate = round(max_v / min_v, 2)

        change_list = ['0' if c < 0 else '1' for c in histndf[0:7]['pct_change']][::-1]
        change_str = ''.join(change_list)

        df_size = len(volumes)
        next_high_arr = []
        next_low_arr = []
        gap_scale = 0
        gap_space = 0
        for index in range(df_size - 1):
            pre_data = histndf.iloc[index + 1]
            next_data = histndf.iloc[index]

            pre_high = pre_data['high']
            pre_low = pre_data['low']
            next_high = next_data['high']
            next_low = next_data['low']

            next_low_arr.append(next_low)
            next_high_arr.append(next_high)

            if index < 3:
                if gap_scale == 0:
                    # 向下跳空缺口
                    if pre_low > max(next_high_arr):
                        gap_scale = round((max(next_high_arr) - pre_low) / max(next_high_arr) * 100, 2)
                        # 计算缺口和现价的空间
                        gap_space = round((current_price - pre_low) / pre_low * 100, 2)
                    # 向上跳空
                    elif min(next_low_arr) > pre_high:
                        gap_scale = round((min(next_low_arr) - pre_high) / pre_high * 100, 2)
                        # 计算缺口和现价的空间
                        gap_space = round((current_price - pre_high) / pre_high * 100, 2)

        item = data_util.get_basics(code)
        idx = item.index.to_numpy()[0]
        nlist = [code, item.at[idx, 'name'], item.at[idx, 'industry'], item.at[idx, 'area'], change_str, gap_scale,
                 gap_space, str(np.round(week_vol, 2)), multi_vol_rate]
        upndata.append(nlist)

    gap_df = pd.DataFrame(upndata,
                         columns=['code', 'name', 'industry', 'area', 'change_7_days', 'gap', 'gap_space',
                                  'multi_vol', 'vol_rate'])
    gap_df = gap_df.sort_values(['gap', 'gap_space'], ascending=[False, True])
    return gap_df


if __name__ == '__main__':
    # codes = ['300123']
    codes = stock_pool
    df = cal_gap(codes=codes)
    # print(df)
    db_util.to_db(df, 'weekly_gap')
