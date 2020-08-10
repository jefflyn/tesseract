import pandas as pd

import stocks.util.db_util as _dt
from stocks.util import date_const
from stocks.util import date_util
from utils.mail import mail_util

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'
    one_year_ago = date_const.ONE_YEAR_AGO_YYYYMMDD
    half_year_ago = date_const.SIX_MONTHS_AGO_YYYYMMDD

    # today limit up
    sql_today_limitup = "select sra.concepts,lud.name,sra.pe,lud.combo,sra.wave_a,sra.wave_b,sra.map," \
                        "lud.code,lud.industry,sra.list_date issue," \
                        "sra.count,sra.wave_detail  " \
                        "from limit_up_daily lud left join select_result_all sra on lud.code = sra.code " \
                        "where lud.trade_date = :latest_date " \
                        "and sra.list_date < :list_date " \
                        "and lud.code not like '688%' and combo >=3 " \
                        "order by combo desc, sra.wave_a"
    df_sql_today_limitup = _dt.read_sql(sql_today_limitup,
                                        params={"latest_date": date_util.get_latest_trade_date()[0],
                                                "list_date": half_year_ago})

    # combo
    sql_combo = "select * from select_x where select_type='combo'"
    df_combo = _dt.read_query(sql_combo)

    # map
    sql_today_map = "select * from select_x where select_type='map'"
    df_today_map = _dt.read_query(sql_today_map)

    # new
    sql_new = "select * from select_x where select_type='new'"
    df_new = _dt.read_query(sql_new)

    select_columns = "select code, area, industry, concepts, pe, profit, list_date, issue_price, price, issue_space, " \
                     "pct, map, name, wave_a, wave_b, count, count_, wave_detail, " \
                     "concat(c30d, ',', cq1, ',', cq2, ', ', cq3,', ',cq4) ct, select_time "
    # all
    sql_all = select_columns + "from select_result_all where name not like :name " \
                               "and list_date < :list_date " \
                               "order by wave_a"
    df_all = _dt.read_sql(sql_all, params={"name": "%ST%", "list_date": one_year_ago})

    # st
    sql_st_select = "select concepts, code, area, industry, pe, name, wave_a, wave_b, count, count_, wave_detail, select_time "
    sql_st = select_columns + "from select_result_all where name like :name " \
                              "order by wave_a"
    df_st = _dt.read_sql(sql_st, params={"name": "%ST%"})

    file_name = 'select_' + date_util.get_today(date_util.FORMAT_FLAT) + '.xlsx'
    writer = pd.ExcelWriter(file_name)

    df_sql_today_limitup.to_excel(writer, sheet_name='limitup')
    df_combo.to_excel(writer, sheet_name='combo')
    df_today_map.to_excel(writer, sheet_name='map')
    df_new.to_excel(writer, sheet_name='new')
    df_all.to_excel(writer, sheet_name='all')
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
