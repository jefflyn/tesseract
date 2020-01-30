from utils.mail import mail_util
import pandas as pd
from stocks.util import date_util
from stocks.gene import limitup


if __name__ == '__main__':
    content = 'Please find the attaches for today up limit report details.'

    df = limitup.get_today_up_limit_count()

    file_name = 'up_limit_' + date_util.get_today(date_util.format_flat) + '.xlsx'
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer, sheet_name='up_limit')

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
