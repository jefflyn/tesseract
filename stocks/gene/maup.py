import datetime

import numpy as np
import pandas as pd

from stocks import util
from stocks.data import data_util

MA_GRADE_10 = 10
MA_GRADE_9 = 9
MA_GRADE_8 = 8
MA_GRADE_7 = 7
MA_GRADE_6 = 6
MA_GRADE_5 = 5
MA_GRADE_4 = 4
MA_GRADE_3 = 3
MA_GRADE_2 = 2
MA_GRADE_1 = 1


def gap_between(a, b, gap=0.2):
    if a >= b or b == -1:
        return True
    ab_gap = round((abs(b) - abs(a)) / abs(a) * 100, 2)
    return abs(ab_gap) <= gap


def get_ma_point(ma_arr=None):
    """
    获取移动平均等级
    :param ma_arr:
    :return:
    """
    price = ma_arr[0]
    ma5 = ma_arr[1]
    ma10 = ma_arr[2]
    ma20 = ma_arr[3]
    ma30 = ma_arr[4]
    ma60 = ma_arr[5]
    ma90 = ma_arr[6]
    ma120 = ma_arr[7]
    ma250 = ma_arr[8]
    # ma_arr = (price, ma5, ma10, ma20, ma30, ma60, ma90, ma120, ma250)
    # ma_std = np.nanstd(ma_arr)
    # print(ma_arr, round(ma_std, 2))
    grade = 0.0

    if gap_between(ma5, ma10) and gap_between(ma10, ma20) and gap_between(ma20, ma30) and gap_between(ma30, ma60) \
            and gap_between(ma60, ma90) and gap_between(ma90, ma120):
    # if ma10 >= ma20 >= ma30 >= ma60 >= ma90 >= ma120 > 0:
        grade = MA_GRADE_9
        if gap_between(ma120, ma250):
            grade = MA_GRADE_10
        space_base = ma250
        index = len(ma_arr)
        while index > 0:
            if space_base > 0:
                break
            else:
                index = index - 1
                space_base = ma_arr[index]

        space = abs(price - space_base) / space_base
        point = (1 - space) if space < 1 else 0
        grade += point
        return grade

    return grade


def get_ma_data(codes=None, start='2017-01-04', end=None):
    starttime = datetime.datetime.now()
    # print("process ma data start at [%s]" % starttime)
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes

    madfdata = []
    for code in code_list:
        hist_data = data_util.get_k_data(code, start=start)
        if hist_data is None or len(hist_data) == 0:
            continue
        latest = hist_data.tail(1)
        idx = latest.index.to_numpy()[0]
        price = latest.at[idx, 'close']
        latest_date_str = latest.at[idx, 'date']
        # excluding halting
        if util.is_halting(code, latest_date_str):
            continue

        ma5 = hist_data.tail(5).mean()['close']
        ma10 = hist_data.tail(10).mean()['close']
        ma20 = hist_data.tail(20).mean()['close']
        ma30 = hist_data.tail(30).mean()['close']
        ma60 = hist_data.tail(60).mean()['close']
        ma90 = hist_data.tail(90).mean()['close']
        ma120 = hist_data.tail(120).mean()['close']
        ma250 = hist_data.tail(250).mean()['close']

        ma30ls = [ma5, ma10, ma20, ma30]
        ma60ls = [ma5, ma10, ma20, ma30, ma60]
        ma120ls = [ma5, ma10, ma20, ma30, ma60, ma90, ma120]
        ma250ls = [ma5, ma10, ma20, ma30, ma60, ma90, ma120, ma250]

        ma30std = np.std(np.array(ma30ls))
        ma60std = np.std(np.array(ma60ls))
        ma120std = np.std(np.array(ma120ls))
        ma250std = np.std(np.array(ma250ls))

        isup = (ma10 >= ma20) & (ma20 >= ma30)

        row = data_util.get_basics(code)
        idx = row.index.to_numpy()[0]
        malist = []
        malist.append(code)
        malist.append(row.at[idx, 'name'])
        malist.append(row.at[idx, 'industry'])
        malist.append(row.at[idx, 'area'])
        malist.append(isup)
        malist.append(price)
        malist.append(round(ma5, 2))
        malist.append(round(ma10, 2))
        malist.append(round(ma20, 2))
        malist.append(round(ma30, 2))
        malist.append(round(ma60, 2))
        malist.append(round(ma90, 2))
        malist.append(round(ma120, 2))
        malist.append(round(ma250, 2))
        malist.append(round(ma30std, 3))
        malist.append(round((price - ma10) / ma10 * 100, 3))
        # malist.append(ma60std)
        # malist.append(ma120std)
        # malist.append(ma250std)

        madfdata.append(malist)

    ma_df = pd.DataFrame(madfdata, columns=['code', 'name', 'industry', 'area', 'isup', 'price', \
                                            'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma90', 'ma120', 'ma250', 'ma30std',
                                            'ma10_space'])  # ,'ma60std','ma120std','ma250std'])
    ma_df = ma_df.sort_values(by=['isup', 'ma10_space'], ascending=[False, True])
    # endtime = datetime.datetime.now()
    # print("process ma data finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return ma_df


if __name__ == '__main__':
    print(gap_between(10, 10.054))
    codes = ['300782']
    # df = get_ma_data(codes, start='2017-01-01')
    df = data_util.get_ma_data(codes)
    print(df)

    ma_arr = (6.69, 6.71, 6.71, 6.63, 6.57, 6.59, 6.80, 6.92, 7.88)
    print(get_ma_point(ma_arr))


