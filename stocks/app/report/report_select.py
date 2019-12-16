from utils.mail import mail_util
import pandas as pd
import stocks.util.db_util as _dt
from stocks.util import date_util

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'

    sql_down = "select * from select_result_all where list_date < 20180901 and pe_ttm is not null and pe_ttm < pe and (wave_a < -50 and wave_b < 15 or wave_b <= -50) and count > 0 and count < 7 order by wave_a"
    df_down = _dt.read_query(sql_down)

    sql_active = "select * from select_result_all where (pe_ttm is not null or pe is not null) and (wave_a < -40 and wave_b < 15 or wave_b <= -30) and count >= 8 and list_date < 20190101 order by count desc, wave_a"
    df_active = _dt.read_query(sql_active)

    writer = pd.ExcelWriter('select.xlsx')
    df_down.to_excel(writer, sheet_name='down')
    df_active.to_excel(writer, sheet_name='active')
    writer.save()

    attaches = []
    att = mail_util.create_attach('select.xlsx')
    attaches.append(att)

    subj = "Stock Selection Report " + date_util.get_today()
    to_users = ['649054380@qq.com']
    ret = mail_util.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully.")
    else:
        print("Email send failed.")
