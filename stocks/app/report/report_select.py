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

    sql_down = select_columns + "from select_result_all where list_date < :list_date " \
                                "and pe > 0 and pe_ttm > 0 " \
                                "and (wave_a < -50 and wave_b < 15 or wave_b <= -50) " \
                                "order by wave_a"
    df_down = _dt.read_sql(sql_down, params={"list_date": one_year_ago})

    sql_active = select_columns + "from select_result_all where list_date < :list_date " \
                                  "and pe > 0 and pe_ttm > 0 " \
                                  "and (wave_a < -35 and wave_b < 15 or wave_b <= -40) " \
                                  "and count >= 8 order by wave_a"
    df_active = _dt.read_sql(sql_active, params={"list_date": one_year_ago})

    sql_chance = select_columns + "from select_result_all where list_date < :list_date " \
                                  "and pe > 0 and pe_ttm > 0 " \
                                  "and last_f_date <> '' " \
                                  "and (wave_a < -35 and wave_b < 15 or wave_b <= -40) " \
                                  "order by wave_a"
    df_chance = _dt.read_sql(sql_chance, params={"list_date": one_year_ago})

    sql_nice = select_columns + r"from select_result_all where name not like :name " \
                               r"and list_date < :list_date and (wave_a < -33 and wave_b < 15) " \
                                r"and map >= 8 and pe > 0 and pe_ttm > 0 and count > 0 order by wave_a"
    df_nice = _dt.read_sql(sql_nice, params={"name": "%ST%", "list_date": one_year_ago})

    sql_all = select_columns + r"from select_result_all where name not like :name " \
                               r"and list_date < :list_date order by wave_a"
    df_all = _dt.read_sql(sql_all, params={"name": "%ST%", "list_date": one_year_ago})

    sql_st = select_columns + r"from select_result_all where name like :name order by wave_a"
    df_st = _dt.read_sql(sql_st, params={"name": "%ST%"})

    sql_new = select_columns + "from select_result_all where list_date >= :list_date order by wave_a"
    df_new = _dt.read_sql(sql_new, params={"list_date": one_year_ago})

    sql_limit_up = "select stat.trade_date 交易日期, stat.code 代码, stat.name 名称, stat.industry 行业, stat.area 地区, " \
                   "stat.pe 市盈率, stat.combo_times as 涨停数,stat.wave_a A波, stat.wave_b B波, stat.turnover_rate 换手率, " \
                   "stat.vol_rate 量比, case when vol_rate < 0.8 then '缩量（不活跃）' " \
                   "when vol_rate >= 0.8 and vol_rate < 1.5 then '正常水准（正常活动）' " \
                   "when vol_rate >= 1.5 and vol_rate < 2.5 then '柔和放量（相对健康）' " \
                   "when vol_rate >= 2.5 and vol_rate < 5 then '明显放量（突破机会）' " \
                   "when vol_rate >= 5 and vol_rate < 10 then '剧烈放量（低位好信号）' " \
                   "when vol_rate >= 10 then '巨量（反向操作）' when vol_rate >= 20 then '极端放量（死亡）' end as 量比解读, " \
                   "open_change 开盘幅度,update_time from limit_up_stat stat inner join basics b on stat.code = b.code " \
                   "where stat.trade_date=:trade_date order by stat.wave_a;"
    df_limit_up = _dt.read_sql(sql_limit_up, params={"trade_date": date_util.get_today()})

    file_name = 'select_' + date_util.get_today(date_util.format_flat) + '.xlsx'
    writer = pd.ExcelWriter(file_name)
    df_limit_up.to_excel(writer, sheet_name='limit')
    df_nice.to_excel(writer, sheet_name='nice')
    df_active.to_excel(writer, sheet_name='active')
    df_chance.to_excel(writer, sheet_name='chance')
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
