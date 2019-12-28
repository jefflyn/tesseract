from stocks.util import display

import datetime
import pandas as pd
from stocks.data import data_util
from stocks.util import db_util
from stocks.util import date_util

LIMITUP_MIN = 9.9
LIMITUP_FROM_DAYS = -365

sql = "select h.trade_date, b.code, h.close, h.open, h.high, h.low, h.pct_change " \
      "from hist_trade_day h inner join basic b on h.ts_code = b.ts_code " \
      "where h.trade_date >='2018-01-01' " \
      "and (h.close = round(h.pre_close * 1.1, 2) or h.pct_change > 9.9)"
histlimitup = db_util.read_query(sql)


def get_today_limitup():
    todayquo = data_util.get_totay_quotations()
    todayquo = todayquo[todayquo['p_change'] >= LIMITUP_MIN]
    return todayquo[['code', 'name', 'p_change']]


def get_limitup_from_hist_trade(codes=None, nature=False, start=None, end=None):
    starttime = datetime.datetime.now()
    if start is None:
        days = datetime.timedelta(LIMITUP_FROM_DAYS)
        start = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')

    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else:
        code_list = codes
    limitupdf = histlimitup[histlimitup.code.isin(code_list)]
    limitupdf = limitupdf[limitupdf.trade_date >= start]
    if limitupdf.empty is True:
        return limitupdf
    if end is not None:
        limitupdf = limitupdf[limitupdf.trade_date <= end]
    if nature:
        limitupdf = limitupdf[limitupdf.high > limitupdf.low]

    return limitupdf


def get_fire_date(date_list=None):
    """
    find the previous date from the continuous trade date
    :param date_list:
    :return: list of previous date
    """
    begin_time = date_util.get_now()
    #print('begin from %s' % str(begin_time))
    if date_list is None:
        return list()
    fire_date_list = list()
    index_flag = 0
    # 需要3个涨停生效，剩下两个不需要处理，所以遍历到倒数第3结束
    index_end = len(date_list) - 2
    for index in range(index_end):
        if index != index_flag:
            continue
        date_str = date_list[index]
        # 连续交易日累加数，大于3有效
        continue_count = 1
        for nxt_index in range(index + 1, len(date_list)):
            nxt_date_str = date_list[nxt_index]
            nxt_date_str_pre = date_util.get_previous_trade_day(nxt_date_str)
            # 如果该交易日是连续的，累加
            if nxt_date_str_pre == date_str:
                continue_count += 1
                date_str = nxt_date_str
            else:
                # 从连续断开的index再遍历
                index_flag = nxt_index
                break
        if continue_count == 3:
            fire_date_list.append(date_list[index])
        elif continue_count > 3:
            fire_date_list.append(date_list[index + 1])
    end_time = date_util.get_now()
    #print("end to %s, total consume time: %s", str(end_time), str((end_time - begin_time).seconds))
    return fire_date_list


def count(df=None):
    """
    count the specific periods limitup 
    :param df: limit data frame
    :return: latest 30 days, last 4 quarters, total 11 months' limitup count
    ['code', 'count', 'count_', 'c30d', 'cq1', 'cq2', 'cq3', 'cq4', 'fdate', 'mindate', 'lldate', 'lup_low', 'lup_high']
    """
    if df.empty:
        return df

    backward_days = -30
    count_data_list = []
    # group by data
    dfgroup = df.groupby('code')
    for code, group in dfgroup:
        count_data = []
        starttime = datetime.datetime.now()
        days = datetime.timedelta(backward_days)
        start30 = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        # #print('latest 30 days limitup from %s' % start30)
        lupdf = group[group.trade_date >= start30]
        count_30d = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 3 + backward_days)
        qrt1st = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        #print('latest 1 quarter limitup from %s' % qrt1st)
        lupdf = group[(group.trade_date >= qrt1st) & (group.trade_date < start30)]
        count_qrt1st = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 6 + backward_days)
        qrt2nd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        #print('latest 2 quarter limitup from %s' % qrt2nd)
        lupdf = group[(group.trade_date >= qrt2nd) & (group.trade_date < qrt1st)]
        count_qrt2nd = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 9 + backward_days)
        qrt3rd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        #print('latest 3 quarter limitup from %s' % qrt3rd)
        lupdf = group[(group.trade_date >= qrt3rd) & (group.trade_date < qrt2nd)]
        count_qrt3rd = lupdf.iloc[:, 0].size

        lupdf = group[group.trade_date < qrt3rd]
        count_qrt4th = lupdf.iloc[:, 0].size

        super_lup = group[group.high == group.low]
        slp_count = super_lup.iloc[:, 0].size
        total_count = group.trade_date.count()
        mindate = group.trade_date.min()
        maxdate = group.trade_date.max()
        low = group.low.min()  # the low in time limitup time zone
        high = group.high.max()

        count_data.append(code)
        count_data.append(total_count)
        count_data.append(slp_count)
        count_data.append(count_30d)
        count_data.append(count_qrt1st)
        count_data.append(count_qrt2nd)
        count_data.append(count_qrt3rd)
        count_data.append(count_qrt4th)
        count_data.append(get_fire_date(list(group['trade_date'])))
        count_data.append(mindate)
        count_data.append(maxdate)
        count_data.append(round(low, 2))
        count_data.append(round(high, 2))
        count_data_list.append(count_data)

    count_result = pd.DataFrame(data=count_data_list,
                                columns=['code', 'count', 'count_', 'c30d', 'cq1', 'cq2', 'cq3', 'cq4', 'fdate',
                                         'mindate', 'lldate', 'lup_low', 'lup_high'])
    count_result = count_result.sort_values('count', axis=0, ascending=False, inplace=False, kind='quicksort',
                                            na_position='last')

    return count_result


if __name__ == '__main__':
    # print(get_fire_date(['2019-01-10', '2019-01-30', '2019-01-31', '2019-02-01', '2019-02-11', '2019-02-12', '2019-02-13',
    #                '2019-02-14', '2019-02-15', '2019-06-17', '2019-06-19', '2019-06-20', '2019-06-21', '2019-11-28',
    #                '2019-11-29', '2019-12-02']))
    # print(get_fire_date(['2019-01-30', '2019-01-31', '2019-02-01']))
    # logger.debug(get_today_limitup())
    # lpdf = get_limitup_from_hist_k(['002813'])
    # #print(lpdf)
    df = get_limitup_from_hist_trade(['600345'])
    #print(df)
    df_count = count(df)
    #print(df_count)
