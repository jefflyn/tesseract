import pandas as pd
import datetime
from stocks.app import report
from stocks.app import _utils
from stocks.data import _datautils
from stocks.data import _reference
from stocks.gene import maup
from stocks.gene import upnday
from stocks.app import selector
from stocks.app import _dateutil


def get_period_change(period_k=None):
    first = period_k.head(1)
    last = period_k.tail(1)
    last_begin_open = first.ix[first.index.get_values()[0], 'open'] if (period_k is not None and len(period_k) > 0) else 0
    last_end_close = last.ix[last.index.get_values()[0], 'close'] if (period_k is not None and len(period_k) > 0) else 0
    last_change = 0
    if last_begin_open > 0:
        last_change = round((last_end_close - last_begin_open) / last_begin_open * 100, 2)
    return last_change

if __name__ == '__main__':
    print('start at', datetime.datetime.now())
    basics = _datautils.get_basics(excludeCyb=False)

    today = _dateutil.get_today()
    last_year_start = _dateutil.get_last_year_start()
    last_year_end = _dateutil.get_last_year_end()

    last_quarter_start = _dateutil.get_last_quarter_start()
    last_quarter_end = _dateutil.get_last_quarter_end()

    last_month_start = _dateutil.get_last_month_start()
    last_month_end = _dateutil.get_last_month_end()

    last_week_start = _dateutil.get_last_week_start()
    last_week_end = _dateutil.get_last_week_end()

    this_year_start = _dateutil.get_this_year_start()
    this_year_end = _dateutil.get_this_year_end()

    this_month_start = _dateutil.get_this_month_start()
    this_month_end = _dateutil.get_this_month_end()

    this_quarter_start = _dateutil.get_this_quarter_start()
    this_quarter_end = _dateutil.get_this_quarter_end()

    this_week_start = _dateutil.get_this_week_start()
    this_week_end = _dateutil.get_this_week_end()

    result_list=[]
    for index, row in basics.iterrows():
        markettime = str(row['timeToMarket']) #exclude new stock
        lastmonth = _dateutil.get_last_month_start('%Y%m%d')
        if markettime > lastmonth:
            continue
        target_k_data = _datautils.get_k_data(index, last_year_start, today)
        if target_k_data is None:
            continue
        last_week_k = target_k_data[(target_k_data.date >= last_week_start) & (target_k_data.date <= last_week_end)]
        this_week_k = target_k_data[(target_k_data.date >= this_week_start) & (target_k_data.date <= this_week_end)]
        last_month_k = target_k_data[(target_k_data.date >= last_month_start) & (target_k_data.date <= last_month_end)]
        this_month_k = target_k_data[(target_k_data.date >= this_month_start) & (target_k_data.date <= this_month_end)]
        last_quarter_k = target_k_data[(target_k_data.date >= last_quarter_start)
                                       & (target_k_data.date <= last_quarter_end)]
        this_quarter_k = target_k_data[(target_k_data.date >= this_quarter_start)
                                       & (target_k_data.date <= this_quarter_end)]
        last_year_k = target_k_data[(target_k_data.date >= last_year_start) & (target_k_data.date <= last_year_end)]
        this_year_k = target_k_data[(target_k_data.date >= this_year_start) & (target_k_data.date <= this_year_end)]

        last_week_change = get_period_change(last_week_k)
        this_week_change = get_period_change(this_week_k)
        last_month_change = get_period_change(last_month_k)
        this_month_change = get_period_change(this_month_k)
        last_quarter_change = get_period_change(last_quarter_k)
        this_quarter_change = get_period_change(this_quarter_k)
        last_year_change = get_period_change(last_year_k)
        this_year_change = get_period_change(this_year_k)

        rec_list=[]
        rec_list.append(row['code'])
        rec_list.append(row['name'])
        rec_list.append(row['industry'])
        rec_list.append(row['area'])
        rec_list.append(markettime)
        rec_list.append(last_week_change)
        rec_list.append(this_week_change)
        rec_list.append(last_month_change)
        rec_list.append(this_month_change)
        rec_list.append(last_quarter_change)
        rec_list.append(this_quarter_change)
        rec_list.append(last_year_change)
        rec_list.append(this_year_change)
        result_list.append(rec_list)
        print(len(result_list))

    result_df = pd.DataFrame(result_list, columns=['代码','名称','行业','地区','上市时间','上周涨幅','本周涨幅','上月涨幅','本月涨幅','上季涨幅','本季涨幅','去年涨幅','今年涨幅'])
    result_df = result_df.sort_values('本周涨幅', ascending=False)
    _datautils.to_db(result_df, 'change_stat')
    print('end at', datetime.datetime.now())

