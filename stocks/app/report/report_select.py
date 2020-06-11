import pandas as pd

import stocks.util.db_util as _dt
from stocks.data import data_util
from stocks.util import date_const
from stocks.util import date_util
from utils.mail import mail_util

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'

    one_year_ago = date_const.ONE_YEAR_AGO_YYYYMMDD

    select_columns = "select code, name, area, industry, concepts, list_date, pe, pe_ttm as profit, pct, map, a_days, " \
                     "wave_a, wave_b, b_days, count, count_, wave_detail, concat(c30d,cq1,cq2,cq3,cq4) ct, select_time "

    # my stock pool
    sql_my_stock = select_columns + "from select_result_all where code in " \
                                    "(select code from my_stock_pool where platform in :platform)" \
                                    "order by wave_a"
    df_my_stock = _dt.read_sql(sql_my_stock, params={"platform": ['pos', 'pa', 'cf', 'df']})

    # today limit up
    limit_up_codes = data_util.get_hist_trade(start=date_util.get_latest_trade_date()[0], is_limit=True)
    if limit_up_codes.empty:
        limit_up_codes = data_util.get_hist_trade(start=date_util.get_previous_trade_day(), is_limit=True)
    sql_today_limitup = select_columns + "from select_result_all where list_date < :list_date and code in :codes" \
                                         "order by wave_a"
    df_sql_today_limitup = _dt.read_sql(sql_today_limitup,
                                        params={"list_date": date_util.get_last_2month_start(),
                                                "codes": list(limit_up_codes['code'])})

    # combo > 3
    sql_combo = select_columns + "from select_result_all where list_date < :list_date and name not like :name " \
                                 "and code in (select code from limit_up_stat where fire_date >= :target_date and combo > :combo) " \
                                 "and (wave_b <= -33 or (wave_b > 0 and wave_b < 20) or (wave_a <= -40 and wave_b < 30)) " \
                                 "order by wave_a"
    df_combo = _dt.read_sql(sql_combo, params={"list_date": one_year_ago, "name": "%ST%",
                                               "target_date": date_util.get_this_year_start(), "combo": 3})

    # pretty ma
    sql_today_ma = select_columns + "from select_result_all where name not like :name " \
                                    "and list_date < :list_date and map > 9 " \
                                    "and (wave_b <= -33 or (wave_a <= -33 and wave_b < 30)) " \
                                    "order by wave_a"
    df_today_ma = _dt.read_sql(sql_today_ma, params={"name": "%ST%", "list_date": one_year_ago})

    # oversold
    sql_oversold = select_columns + "from select_result_all where list_date < :list_date and name not like :name " \
                                    "and pe > 0 and count > 0 " \
                                    "and (wave_a <= -50 and wave_b < 15 or wave_b <= -50) " \
                                    "order by wave_a"
    df_oversold = _dt.read_sql(sql_oversold, params={"list_date": one_year_ago, "name": "%ST%"})

    # active
    sql_active = select_columns + "from select_result_all where list_date < :list_date and name not like :name " \
                                  "and pe > 0 and count >= 8 " \
                                  "and (wave_a <= -40 and wave_b < 15 or wave_b <= -40) " \
                                  "order by wave_a"
    df_active = _dt.read_sql(sql_active, params={"list_date": one_year_ago, "name": "%ST%"})

    # all
    sql_all = select_columns + "from select_result_all where name not like :name " \
                               "and list_date < :list_date " \
                               "order by wave_a"
    df_all = _dt.read_sql(sql_all, params={"name": "%ST%", "list_date": one_year_ago})

    # new
    sql_new = select_columns + "from select_result_all where list_date >= :list_date " \
                               "order by wave_a"
    df_new = _dt.read_sql(sql_new, params={"list_date": one_year_ago})

    # st
    sql_st = select_columns + "from select_result_all where name like :name " \
                              "order by wave_a"
    df_st = _dt.read_sql(sql_st, params={"name": "%ST%"})

    file_name = 'select_' + date_util.get_today(date_util.FORMAT_FLAT) + '.xlsx'
    writer = pd.ExcelWriter(file_name)

    df_my_stock.to_excel(writer, sheet_name='my')
    df_sql_today_limitup.to_excel(writer, sheet_name='limitup')
    df_today_ma.to_excel(writer, sheet_name='ma')
    df_combo.to_excel(writer, sheet_name='combo')
    df_active.to_excel(writer, sheet_name='active')
    df_all.to_excel(writer, sheet_name='all')
    df_oversold.to_excel(writer, sheet_name='oversold')
    df_new.to_excel(writer, sheet_name='new')
    df_st.to_excel(writer, sheet_name='st')

    writer.save()

    attaches = []
    att = mail_util.create_attach(file_name)
    attaches.append(att)

    subj = "Stock Selection Report " + date_util.get_today()
    to_users = ['649054380@qq.com']
    ret = mail_util.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully.")
    else:
        print("Email send failed.")
