import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import pandas as pd

from stocks.app import realtime
from stocks.app import falco
from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import period
from stocks.gene import maup
from stocks.gene import bargain

sender = '649054380@qq.com'
passw = 'pznntikuyzfvbchb'
to_users = '649054380@qq.com'
#to_users = ['649054380@qq.com', '1677258052@qq.com','53985188@qq.com']

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')

def generate_report(title=None, df=None, uad=False, ma=False, lup=False):
    html_content = '<h3>' + title + '</h3>'
    html_content += '<h4>1.realtime info:</h4>'
    # 1.realtime info
    codes = list(df['code'])
    rtdf = falco.get_monitor(codes)
    rtdf = rtdf[['warn','code','name','change','price','low','bottom','space','industry','area','pe']]

    rtdf = rtdf.sort_values('space', ascending=False)
    rtdf_html = rtdf.to_html(escape=False, index=False, sparsify=True, border=1, index_names=False, header=True)
    html_content += rtdf_html

    codes = list(rtdf.code)
    names = list(rtdf.name)
    stkdict = dict(zip(codes, names))
    # 2.up-and-down price of recent 1 year
    if uad == True:
        html_content += '<h4>2.up-and-down price of recent 1 year:</h4>'
        wavedf = period.get_wave(codes, start='2017-01-01')
        wavedf = wavedf.replace(stkdict)
        wavedf_html = wavedf.to_html(escape=False, index=False, sparsify=True, border=1, index_names=False, header=True)
        html_content += wavedf_html

    # 3.moving average prices of several crucial periods
    if ma == True:
        html_content += '<h4>3.moving average prices of several crucial periods:</h4>'
        madf = maup.get_ma(codes, start='2017-01-01')
        madf_html = madf.to_html(escape=False, index=False, sparsify=True, border=1, index_names=False, header=True)

        maupdf = maup.get_ma_up(madf)
        maupdf_html = maupdf.to_html(escape=False, index=False, sparsify=True, border=1, index_names=False, header=True)
        html_content += (madf_html + maupdf_html)

    # 4.limit-up of recent 1 year
    if lup == True:
        html_content += '<h4>4.limit-up of recent 1 year:</h4>'
        limitupdf = limitup.get_limit_up(codes, start='2017-01-01')
        limitupdf = limitupdf.replace(stkdict)
        limitupdf_html = limitupdf.to_html(escape=False, index=False, sparsify=True, border=1, index_names=False,
                                           header=True)
        html_content += limitupdf_html

    return html_content


def mail(to_users=[], content=None):
    ret = True
    try:
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", sender])  # sender nickname and account
        #msg['To'] = formataddr(["FK", to_users])  # receiver nickname and account
        msg['Subject'] = todaystr + " Stocks Report"  # subject

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  #SMTP server and port
        server.login(sender, passw)
        server.sendmail(sender, to_users, msg.as_string())
        server.quit()  # close connection
    except Exception:
        ret = False
    return ret


subnewdf = _datautils.get_subnew(excludeCyb=True)
subnewdf = generate_report(title='The sub-new stocks report', df=subnewdf, uad=True, ma=True, lup=True)
content = mail(to_users, content)
if ret:
    print("Email send successfully")
else:
    print("Send failed")

if __name__ == '__main__':
    print()
