import datetime
import pandas as pd
from stocks.data import data_util
from stocks.base import db_util
from stocks.base import display
from stocks.base.logging import logger

LIMITUP_MIN = 9.9
LIMITUP_FROM_DAYS = -365

sql = "select h.trade_date, b.code, h.close, h.open, h.high, h.low, h.pct_change " \
      "from hist_trade_day h inner join basic b on h.ts_code = b.ts_code " \
      "where h.trade_date >='2018-01-01' and h.close = round(h.pre_close * 1.1, 2)"
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


def count(df=None):
    """
    count the specific periods limitup 
    :param df: limit data frame
    :return: latest 30 days, last 4 quarters, total 11 months' limitup count
    """
    if df.empty:
        return df

    backward_days = -30
    count_data_list = []
    # group by data
    dfgroup = df.groupby('code')
    for name, group in dfgroup:
        count_data = []
        starttime = datetime.datetime.now()
        days = datetime.timedelta(backward_days)
        start30 = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        logger.debug('latest 30 days limitup from %s' % start30)
        lupdf = group[group.trade_date >= start30]
        count_30d = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 3 + backward_days)
        qrt1st = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        logger.debug('latest 1 quarter limitup from %s' % qrt1st)
        lupdf = group[(group.trade_date >= qrt1st) & (group.trade_date < start30)]
        count_qrt1st = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 6 + backward_days)
        qrt2nd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        logger.debug('latest 2 quarter limitup from %s' % qrt2nd)
        lupdf = group[(group.trade_date >= qrt2nd) & (group.trade_date < qrt1st)]
        count_qrt2nd = lupdf.iloc[:, 0].size

        days = datetime.timedelta(backward_days * 9 + backward_days)
        qrt3rd = datetime.datetime.strftime(starttime + days, '%Y-%m-%d')
        logger.debug('latest 3 quarter limitup from %s' % qrt3rd)
        lupdf = group[(group.trade_date >= qrt3rd) & (group.trade_date < qrt2nd)]
        count_qrt3rd = lupdf.iloc[:, 0].size

        lupdf = group[group.trade_date < qrt3rd]
        count_qrt4th = lupdf.iloc[:, 0].size

        size = group.trade_date.count()
        mindate = group.trade_date.min()
        maxdate = group.trade_date.max()
        low = group.low.min()  # the low in time limitup time zone
        high = group.high.max()

        count_data.append(name)
        count_data.append(size)
        count_data.append(count_30d)
        count_data.append(count_qrt1st)
        count_data.append(count_qrt2nd)
        count_data.append(count_qrt3rd)
        count_data.append(count_qrt4th)
        count_data.append(mindate)
        count_data.append(maxdate)
        count_data.append(round(low, 2))
        count_data.append(round(high, 2))
        count_data_list.append(count_data)

    count_result = pd.DataFrame(data=count_data_list,
                                columns=['code', 'count', 'c30d', 'cq1', 'cq2', 'cq3', 'cq4',
                                         'mindate', 'lldate', 'lup_low', 'lup_high'])
    count_result = count_result.sort_values('count', axis=0, ascending=False, inplace=False, kind='quicksort',
                                            na_position='last')

    return count_result


if __name__ == '__main__':
    logger.debug(get_today_limitup())

    # lpdf = get_limitup_from_hist_k(['002813'])
    # print(lpdf)
    df = get_limitup_from_hist_trade(['600405'])
    print(df)
    dfcount = count(df)
    print(dfcount)
