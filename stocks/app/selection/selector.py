import sys
from datetime import datetime as dt
from sys import argv

import pandas as pd

import stocks.util.db_util as _dt
from stocks.data import data_util
from stocks.data.service import concept_service
from stocks.gene import limitup
from stocks.gene import upnday
from stocks.gene import wave
from stocks.util import date_const
from stocks.util import date_util
from stocks.util._utils import timer

last_trade_date = date_util.get_latest_trade_date(1)[0]

this_week_hist = data_util.get_hist_trade_high_low(start=date_const.FIRST_DAY_THIS_WEEK,
                                                           end=date_const.LAST_DAY_THIS_WEEK)
# from stocks.data.service import hist_trade_service
# open_date_map = hist_trade_service.get_new_open_date()

@timer
def select_from_all(fname='all'):
    """
    select all stocks
    :param fname: all
    :return: 
    """
    select_result(filename=fname)


def sync_select_rds():
    '''
    同步select到rds
    :return:
    '''
    select_df = _dt.read_query("select * from select_result_all order by industry, wave_a")
    _dt.to_db(data=select_df, tbname='select_result_all', db_engine='rds')


def select_result(codeset=None, filename=''):
    begin_time = date_util.now()
    if (codeset is None or len(codeset) == 0) and filename != 'all':
        return
    trade_date_list = date_util.get_latest_trade_date(4)
    hist_trade_df = None
    curt_trade_date = None
    for trade_date in trade_date_list:
        hist_trade_df = data_util.get_hist_trade(code=codeset, start=trade_date, end=last_trade_date)
        if len(hist_trade_df) > 0:
            print('get latest trade: %s' % trade_date)
            curt_trade_date = trade_date
            break

    if codeset is not None:
        size = len(codeset)
    else:
        size = len(hist_trade_df.index.to_numpy())
    print('select stocks start! total size: %d\n' % size)
    data_list = []
    # 概念信息
    concepts = concept_service.get_concepts()
    basics = data_util.get_basics()
    # fundamentals = fundamental_service.get_fundamental()
    wavedfset = pd.DataFrame(columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'change'])
    ma_data_df = data_util.get_ma_data(trade_date=curt_trade_date)
    issue_df = data_util.get_issue_price()
    for index, row in hist_trade_df.iterrows():
        code = row['code']
        if str(code)[:3] == '688':
            continue

        if index % 100 == 0:
            print('count down from ' + str(size) + ' >>> processing ' + code)
        size -= 1
        open = float(row['open'])
        current_price = float(row['close'])
        # maybe in trading halt or others situation, ignore this code
        if open <= 0 or current_price <= 0:
            continue

        curt_data = list()
        concept = concepts[concepts.code == code]
        fundamental = basics[basics.code == code]

        curt_data.append(concept.loc[code, 'concepts'] if concept.empty is False else '')
        curt_data.append(round(fundamental.loc[code, 'pe'], 1) if fundamental.empty is False else 0)
        # curt_data.append(round(fundamental.loc[code, 'pe_ttm'], 1) if fundamental.empty is False else 0)
        curt_data.append(fundamental.loc[code, 'profit'])  # pe_ttm
        # curt_data.append(fundamental.loc[code, 'turnover_rate'] if fundamental.empty is False else 0)
        curt_data.append(0)

        curt_data.append(code)
        curt_data.append(fundamental.loc[code, 'name'])
        curt_data.append(fundamental.loc[code, 'industry'])
        curt_data.append(fundamental.loc[code, 'area'])
        list_date = str(fundamental.loc[code, 'list_date'])
        issue_price = issue_df.loc[code, 'issue_price']
        issue_space = round((current_price - issue_price) / issue_price * 100, 2)
        is_new = False
        if list_date >= date_const.ONE_YEAR_AGO_YYYYMMDD:
            is_new = True
        curt_data.append(list_date)
        curt_data.append(issue_price)
        curt_data.append(current_price)
        curt_data.append(issue_space)
        curt_data.append(round(float(row['pct_change']), 2))
        # get wave data and bottom top
        # if is_new:
        #     open_date = open_date_map[code] if code in open_date_map.keys() else None
        #     wave_df = wave.get_wave(code, start=open_date)
        # else:
        wave_df = wave.get_wave(code)  # need to save
        if wave_df is None or wave_df.empty is True:
            continue
        wave_size = 10
        # if filename == 'subnew':
        #     wave_size = 10
        wavestr = wave.wave_to_str(wave_df, wave_size)
        wave_ab = wave.get_wave_ab_fast(wavestr, 33)
        wave_a = wave_ab[0][0]
        wave_b = wave_ab[1][0]
        wavedfset = wavedfset.append(wave_df)
        bottomdf = wave.get_bottom(wave_df)
        if bottomdf is None or bottomdf.empty is True:
            continue
        bottom = bottomdf.at[0, 'bottom']
        top = bottomdf.at[0, 'top']
        uspace = (current_price - bottom) / bottom * 100
        dspace = (current_price - top) / top * 100
        position = (current_price - bottom) / (top - bottom) * 100

        curt_data.append(wavestr.split('\n')[0])
        curt_data.append(round(wave_a, 2))
        curt_data.append(wave_ab[0][1])
        curt_data.append(round(wave_b, 2))
        curt_data.append(wave_ab[1][1])
        curt_data.append(bottom)
        curt_data.append(round(uspace, 2))
        curt_data.append(round(dspace, 2))
        curt_data.append(round(top, 2))

        curt_data.append(round(position, 2))
        curt_data.append(round(bottomdf.at[0, 'buy1'], 2))
        curt_data.append(round(bottomdf.at[0, 'buy2'], 2))
        curt_data.append(round(bottomdf.at[0, 'buy3'], 2))

        # limit up data
        limitupdf = limitup.get_limitup_from_hist_trade(code)

        # l1 = l1.append(lupdf, ignore_index=True)
        # l2 = l2.append(limitupdf, ignore_index=True)

        lupcount = 0
        lup_count = 0
        lupcount30 = 0
        lupcountq1 = 0
        lupcountq2 = 0
        lupcountq3 = 0
        lupcountq4 = 0
        fire_dates = []
        last_f_date = ''
        call_prices = []
        call_price = 0
        call_diff = 0
        luplow = 0
        luphigh = 0
        lupcountdf = limitup.count(limitupdf)
        if lupcountdf.empty is False:
            lupcount = lupcountdf.at[0, 'count']
            lup_count = lupcountdf.at[0, 'count_']
            lupcount30 = lupcountdf.at[0, 'c30d']
            lupcountq1 = lupcountdf.at[0, 'cq1']
            lupcountq2 = lupcountdf.at[0, 'cq2']
            lupcountq3 = lupcountdf.at[0, 'cq3']
            lupcountq4 = lupcountdf.at[0, 'cq4']
            fire_dates = lupcountdf.at[0, 'fdate']
            luplow = lupcountdf.at[0, 'lup_low']
            luphigh = lupcountdf.at[0, 'lup_high']

            for fire_date in fire_dates:
                fire_pre_hist = data_util.get_pre_hist_trade(code, fire_date)
                if fire_pre_hist.empty is False:
                    fire_pre_close = fire_pre_hist.at[0, 'close']
                    call_prices.append('<=' + str(fire_pre_close))
                    call_price = fire_pre_close

        curt_data.append(lupcount)
        curt_data.append(lup_count)
        curt_data.append(lupcount30)
        curt_data.append(lupcountq1)
        curt_data.append(lupcountq2)
        curt_data.append(lupcountq3)
        curt_data.append(lupcountq4)
        if len(fire_dates) > 0:
            last_f_date = fire_dates[-1]
            call_diff = round((current_price - call_price) / current_price * 100, 2)
            if (date_util.convert_to_date(list_date) - date_util.convert_to_date(last_f_date)).days == 0:
                fire_dates = ''
                last_f_date = ''
                call_prices = ''
                call_diff = 0
        curt_data.append(str(fire_dates))
        curt_data.append(last_f_date)
        curt_data.append(str(call_prices))
        curt_data.append(call_diff)

        curt_data.append(luplow)
        curt_data.append(luphigh)

        # up n day data
        upndaydf = upnday.get_upnday(code)
        updays = 0
        sumup = 0
        multi_vol_rate = 1
        vol_rate = 0
        change_7_days = ''
        sum_30_days = 0
        gap = 0
        if upndaydf.empty is False:
            change_7_days = upndaydf.at[0, 'change_7_days']
            gap = upndaydf.at[0, 'gap']
            gap_space = upndaydf.at[0, 'gap_space']
            sum_30_days = upndaydf.at[0, 'sum_30_days']
            updays = upndaydf.at[0, 'updays']
            sumup = upndaydf.at[0, 'sumup']
            multi_vol_rate = upndaydf.at[0, 'multi_vol']
            vol_rate = upndaydf.at[0, 'vol_rate']
        curt_data.append(change_7_days)
        curt_data.append(gap)
        curt_data.append(gap_space)
        curt_data.append(sum_30_days)
        curt_data.append(updays)
        curt_data.append(sumup)
        curt_data.append(multi_vol_rate)
        curt_data.append(vol_rate)

        week_hist = data_util.get_hist_week(code=code, n=2)
        week_gap = 0
        late_week_low = 0
        late_week_high = 0
        if week_hist.empty is False and week_hist.shape[0] > 1:
            # 向上跳空缺口
            late_week_low = week_hist.loc[0, 'low']
            pre_week_high = week_hist.loc[1, 'high']
            if late_week_low > pre_week_high:
                week_gap = (late_week_low - pre_week_high) / pre_week_high * 100

            # 向下跳空缺口
            late_week_high = week_hist.loc[0, 'high']
            pre_week_low = week_hist.loc[1, 'low']
            if late_week_high < pre_week_low:
                week_gap = (late_week_high - pre_week_low) / pre_week_low * 100

        curt_data.append(round(week_gap, 2))

        c_week_gap = 0
        c_this_week_hist = this_week_hist[this_week_hist.code == code]
        if c_this_week_hist.empty is False:
            curt_week_low = c_this_week_hist.iloc[0, 2]
            curt_week_high = c_this_week_hist.iloc[0, 1]
            if curt_week_low > late_week_high > 0:
                c_week_gap = (curt_week_low - late_week_high) / late_week_high * 100
            # 向下跳空缺口
            if curt_week_high < late_week_low and late_week_low > 0:
                c_week_gap = (curt_week_high - late_week_low) / late_week_low * 100

        curt_data.append(round(c_week_gap, 2))

        # get maup data
        ma_df = ma_data_df[ma_data_df.code == code]
        curt_data.append(round(ma_df.iloc[0, 2] if ma_df.empty is False else 0, 2))

        # curt_data.append(maupdf.at[0, 'isup'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma5'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma10'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma20'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma30'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma60'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma90'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma120'] if maupdf.empty is False else 0)
        # curt_data.append(maupdf.at[0, 'ma250'] if maupdf.empty is False else 0)

        data_list.append(curt_data)
    columns = ['concepts', 'pe', 'profit', 'turnover_rate', 'code', 'name', 'industry', 'area', 'list_date',
               'issue_price', 'price', 'issue_space', 'pct', 'wave_detail', 'wave_a', 'a_days', 'wave_b', 'b_days',
               'bottom', 'uspace', 'dspace', 'top', 'position', 'buy1', 'buy2', 'buy3', 'count', 'count_',
               'c30d', 'cq1', 'cq2', 'cq3', 'cq4', 'fdate', 'last_f_date',
               'call_price', 'call_diff', 'lup_low', 'lup_high', 'change_7d', 'gap', 'gap_space', 'sum_30d',
               'updays', 'sumup', 'multi_vol', 'vol_rate', 'w_gap', 'c_gap', 'map']
    resultdf = pd.DataFrame(data_list, columns=columns)
    # resultdf = resultdf.sort_values('sum_30d', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')

    resultdf = resultdf[
        ['concepts',  'code', 'name', 'industry', 'area', 'list_date', 'issue_price', 'price', 'issue_space', 'pe', 'profit',
         'pct', 'wave_a', 'wave_b', 'map', 'count', 'count_',
         'wave_detail', 'a_days', 'b_days', 'bottom', 'uspace', 'dspace', 'top', 'position',
         'w_gap', 'c_gap',
         'gap', 'gap_space', 'sum_30d', 'c30d', 'cq1', 'cq2', 'cq3', 'cq4',
         'fdate', 'last_f_date', 'call_price', 'call_diff', 'lup_low', 'lup_high',
         'buy1', 'buy2', 'buy3', 'change_7d', 'updays', 'sumup', 'vol_rate', 'multi_vol', 'turnover_rate']]
    resultdf['trade_date'] = last_trade_date
    resultdf['select_time'] = dt.now()
    result_name = 'select_result_' + filename
    try:
        _dt.to_db(resultdf, result_name)
        _dt.to_db(wavedfset, 'select_wave_' + filename)
    except Exception as e:
        print('save db failed, msg=' + str(e))
        writer = pd.ExcelWriter(filename + '.xlsx')
        resultdf.to_excel(writer, sheet_name='select')
        wavedfset.to_excel(writer, sheet_name='wave')
        writer.save()
        print('save excel success')
    end_time = date_util.now()
    print('select stocks finished, consume time %d secs! result size: %d\n' %
                ((end_time - begin_time).seconds, len(resultdf.index.to_numpy())))
    return resultdf


if __name__ == '__main__':
    print(select_result('300837'))
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
        sys.exit(0)
    codes = argv[1]

    result = select_result(codes)
    # print(result)
