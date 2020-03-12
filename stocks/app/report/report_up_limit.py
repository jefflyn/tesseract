import pandas as pd

from stocks.gene import limitup
from stocks.util import date_util
from stocks.util import db_util
from utils.mail import mail_util

if __name__ == '__main__':
    content = 'Please find the attaches for today up limit report details.'

    df = limitup.get_today_up_limit_count(2)
    df.index = df['code']

    select_columns = "select code,name,industry,pe,pe_ttm,pct,list_date,a_days,wave_a,wave_b,b_days,w_gap,c_gap,map," \
                     "count,count_,fdate,last_f_date,price,call_price,call_diff,concepts,select_time "
    codes = list(df['code'])
    sql_up_limit = select_columns + "from select_result_all where code in :codes "
    df_up_limit = db_util.read_sql(sql_up_limit, params={"codes": codes})
    df_up_limit.index = df_up_limit['code']

    file_name = 'up_limit_' + date_util.get_today(date_util.FORMAT_FLAT) + '.xlsx'
    writer = pd.ExcelWriter(file_name)
    # df.to_excel(writer, sheet_name='up_limit')
    df = df.drop('code', 1)
    result = df.join(df_up_limit)
    result.to_excel(writer, sheet_name='select_up_limit')

    writer.save()

    attaches = []
    att = mail_util.create_attach(file_name)
    attaches.append(att)

    subj = "Stock Up Limit Report " + date_util.get_today()
    to_users = ['649054380@qq.com']
    ret = mail_util.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully.")
    else:
        print("Email send failed.")
