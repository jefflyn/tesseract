import pandas as pd

import stocks.util.db_util as _dt
from stocks.util import date_const
from stocks.util import date_util
from utils.mail import mail_util

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'

    one_year_ago = date_const.ONE_YEAR_AGO_YYYYMMDD

    # index_sql = "select l.*, i.hz, i.sz50, i.scz, i.zxb, i.cyb from (select trade_date, count(case when close >= round(pre_close * 1.1, 2) then 1 else null end) as limitup,        count(case when close <= round(pre_close * 0.9, 2) then 1 else null end) as limitdown,        count(1) as total,        count(case when pct_change > 0 then 1 else null end) as up,        count(case when pct_change = 0 then 1 else null end) as flat,        count(case when pct_change < 0 then 1 else null end) as down from hist_trade_day where trade_date >= '2019-12-01' group by trade_date) as l left join     (select trade_date,        sum(case ts_code when '000001.SH' then pct_change else 0 end) 'hz',        sum(case ts_code when '000016.SH' then pct_change else 0 end) 'sz50',        sum(case ts_code when '399001.SZ' then pct_change else 0 end) 'scz',        sum(case ts_code when '399005.SZ' then pct_change else 0 end) 'zxb',        sum(case ts_code when '399006.SZ' then pct_change else 0 end) 'cyb'       from hist_index_day where trade_date >= '2019-06-01' group by trade_date) as i on l.trade_date = i.trade_date order by l.trade_date desc"
    # df_index = _dt.read_query(index_sql)

    select_columns = "select code,name,industry,concepts,pe,pe_ttm as profit,pct,list_date,a_days,wave_a,wave_b,b_days,w_gap,c_gap,map," \
                     "count,count_,fdate,last_f_date,price,call_price,call_diff,select_time "
    # 超跌
    sql_down = select_columns + "from select_result_all where list_date < :list_date and name not like :name " \
                                "and pe > 0 and count > 0 " \
                                "and (wave_a <= -50 and wave_b < 15 or wave_b <= -50) " \
                                "order by wave_a"
    df_down = _dt.read_sql(sql_down, params={"list_date": one_year_ago, "name": "%ST%"})

    # 活跃
    sql_active = select_columns + "from select_result_all where list_date < :list_date and name not like :name " \
                                  "and pe > 0 and count >= 8 " \
                                  "and (wave_a <= -40 and wave_b < 15 or wave_b <= -40) " \
                                  "order by wave_a"
    df_active = _dt.read_sql(sql_active, params={"list_date": one_year_ago, "name": "%ST%"})

    # all
    sql_all = select_columns + "from select_result_all where name not like :name and list_date < :list_date order by wave_a"
    df_all = _dt.read_sql(sql_all, params={"name": "%ST%", "list_date": one_year_ago})

    # st
    sql_st = select_columns + r"from select_result_all where name like :name order by wave_a"
    df_st = _dt.read_sql(sql_st, params={"name": "%ST%"})

    # new
    sql_new = select_columns + "from select_result_all where list_date >= :list_date order by wave_a"
    df_new = _dt.read_sql(sql_new, params={"list_date": one_year_ago})

    # combo > 1 in last two months
    sql_combo = select_columns + "from select_result_all where pe > 0 " \
                               "and (wave_b < -33 or (wave_b > 0 and wave_b < 20) or (wave_a < -40 and wave_b < 30)) " \
                               "and code in (select code from limit_up_stat where fire_date >= :target_date and combo > 1) " \
                               "order by wave_a;"
    df_combo = _dt.read_sql(sql_combo, params={"target_date": date_util.get_last_2month_start()})

    # today limit up
    sql_today_limit_up = select_columns + "from select_result_all where " \
                                          "code in (select code from limit_up_stat where late_date =:today_str) " \
                                          "and (wave_b < -33 or (wave_b > 0 and wave_b < 20) or (wave_a < -40 and wave_b < 30)) " \
                                          "order by wave_a;"
    df_today_limit_up = _dt.read_sql(sql_today_limit_up, params={"today_str": date_util.get_today()})

    # down to limit low stat
    sql_limit_up = "select * from limit_up_stat where 1=1 and price <= fire_price * 1.05 and combo > 1 " \
                   "and fire_date >= :target_date order by wave_a;"
    df_limit_up = _dt.read_sql(sql_limit_up, params={"target_date": date_util.get_last_month_start()})

    file_name = 'select_' + date_util.get_today(date_util.FORMAT_FLAT) + '.xlsx'
    writer = pd.ExcelWriter(file_name)
    df_today_limit_up.to_excel(writer, sheet_name='today')
    df_combo.to_excel(writer, sheet_name='combo')
    df_limit_up.to_excel(writer, sheet_name='limitup')
    df_active.to_excel(writer, sheet_name='active')
    df_down.to_excel(writer, sheet_name='down')
    df_all.to_excel(writer, sheet_name='all')
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
