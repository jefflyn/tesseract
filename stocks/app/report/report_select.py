import pandas as pd

import stocks.util.db_util as _dt
from stocks.util import date_const
from stocks.util import date_util
from utils.mail import mail_util

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'

    one_year_ago = date_const.ONE_YEAR_AGO_YYYYMMDD

    select_columns = "select code, name, area, industry, concepts, pe, profit, list_date, issue_price, price, issue_space, pct, map, " \
                     "wave_a, wave_b, count, count_, wave_detail, " \
                     "concat(c30d, ',', cq1, ',', cq2, ', ', cq3,', ',cq4) ct, select_time "


    # today limit up
    sql_today_limitup = "select sra.concepts, lud.code,lud.name,lud.industry,sra.list_date issue,sra.pe,sra.map,lud.combo,sra.count," \
                        "sra.wave_a,sra.wave_b, sra.wave_detail  " \
                        "from limit_up_daily lud left join select_result_all sra on lud.code = sra.code " \
                        "where lud.trade_date = :latest_date and sra.list_date < 20200301 and lud.code not like '688%' " \
                        "order by lud.industry, sra.wave_a asc"
    df_sql_today_limitup = _dt.read_sql(sql_today_limitup,
                                        params={"latest_date": date_util.get_latest_trade_date()[0]})

    # combo >= 4
    sql_combo = 'select sra.concepts, sra.code,sra.name,sra.industry ind,sra.list_date issue,sra.pe,lus.combo cbo,' \
                'sra.wave_a wa,sra.wave_b wb,' \
                'round((lus.price - lus.fire_price) / lus.fire_price * 100, 2) fs, sra.map mp, ' \
                'sra.count c, sra.count_ c_, lus.fire_date, lus.late_date, lus.fire_price fprice, lus.price, ' \
                'sra.wave_detail ' \
                'from select_result_all sra join limit_up_stat lus on sra.code=lus.code ' \
                'where sra.name not like :name and sra.list_date < 20200301 and lus.combo >= 4 ' \
                'and (sra.wave_a  < -33 and sra.wave_b  < 20 or sra.wave_b <= -33)' \
                'order by wa'

    df_combo = _dt.read_sql(sql_combo, params={"name": "%ST%"})

    # pretty ma
    sql_today_ma = select_columns + "from select_result_all where name not like :name " \
                                    "and list_date < :list_date and count > 0 " \
                                    "and (map > 10.85 or (map > 10 and wave_a < -33 and wave_b < 40)) " \
                                    "order by map desc, wave_a"
    df_today_ma = _dt.read_sql(sql_today_ma, params={"name": "%ST%", "list_date": one_year_ago})

    # all
    sql_all = select_columns + "from select_result_all where name not like :name " \
                               "and list_date < :list_date " \
                               "order by wave_a"
    df_all = _dt.read_sql(sql_all, params={"name": "%ST%", "list_date": one_year_ago})

    # new
    sql_new = select_columns + "from select_result_all where list_date >= :list_date " \
                               "order by issue_space, wave_a"
    df_new = _dt.read_sql(sql_new, params={"list_date": 20180101})

    # st
    sql_st = select_columns + "from select_result_all where name like :name " \
                              "order by wave_a"
    df_st = _dt.read_sql(sql_st, params={"name": "%ST%"})

    file_name = 'select_' + date_util.get_today(date_util.FORMAT_FLAT) + '.xlsx'
    writer = pd.ExcelWriter(file_name)

    df_sql_today_limitup.to_excel(writer, sheet_name='limitup')
    df_combo.to_excel(writer, sheet_name='combo')
    df_today_ma.to_excel(writer, sheet_name='ma')
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
