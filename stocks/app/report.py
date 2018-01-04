import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header
from IPython.display import HTML
import re
import numpy as np
import pandas as pd

from stocks.app import realtime
from stocks.app import falco
from stocks.app import _utils
from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import period
from stocks.gene import maup
from stocks.gene import bargain

sender = '649054380@qq.com'
passw = 'pznntikuyzfvbchb'
#to_users = '649054380@qq.com'
#to_users = ['649054380@qq.com', '1677258052@qq.com','53985188@qq.com']

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')

def HTML_with_style(df, style=None, random_id=None):
    df_html = df.to_html(index=False, index_names=False)

    if random_id is None:
        random_id = 'id%d' % np.random.choice(np.arange(1000000))

    if style is None:
        style = """
        <style>
            table#{random_id} {{border-collapse:collapse; border-width: 1px; border-style: solid; border-color: rgb(235, 242, 224);}}
            table#{random_id} thead, table#{random_id} tr {{border-top-width: 1px; text-align:right;}}
            table#{random_id} td, table#{random_id} th {{word-break: keep-all; padding: 5px 10px; font-size: 12px; font-family: Verdana;}}
            table#{random_id} tr:nth-child(even) {{background: rgb(230, 238, 214);}}
            table#{random_id} tr:nth-child(odd) {{background: #FFF;}}
        </style>
        """.format(random_id=random_id)
    else:
        new_style = []
        s = re.sub(r'</?style>', '', style).strip()
        for line in s.split('\n'):
                line = line.strip()
                if not re.match(r'^table', line):
                    line = re.sub(r'^', 'table ', line)
                new_style.append(line)
        new_style = ['<style>'] + new_style + ['</style>']

        style = re.sub(r'table(#\S+)?', 'table#%s' % random_id, '\n'.join(new_style))

    df_html = re.sub(r'<table', r'<table id=%s ' % random_id, df_html)

    return style + df_html

def generate_report(title=None, filename=None, monitor=False, uad=False, ma=False, lup=False):
    html_content = '<h3>' + title + '</h3>'
    html_content += '<h4>1.realtime info:</h4>'
    # 1.realtime info

    rtdf = None
    if monitor == False:
        rtdf = realtime.get_realtime(filename, sortby='b')
        rtdf = rtdf[
            ['warn', 'code', 'name', 'price', 'change', 'low', 'bottom', 'btm_space', 'cost', 'profit_amt', 'profit_perc', 'total_amt']]
        # rtdf.columns = ['a', 'b', 'c']
        rtdf.rename(
            columns={'btm_space': 'space', 'profit_amt': 'profit', 'profit_perc': 'percent', 'total_amt': 'amount'}, inplace=True)
    else:
        df = _datautils.get_data('../data/' + filename, sep=' ')
        codes = list(df['code'])
        rtdf = falco.get_monitor(codes)
        rtdf = rtdf[['warn','code','name','change','price','low','bottom','space','industry','area','pe']]

    # rtdf = rtdf.sort_values('space', ascending=False)
    codes = list(rtdf.code)
    names = list(rtdf.name)
    stkdict = dict(zip(codes, names))
    codes.reverse()

    #style format
    # rtdf['code'] = rtdf['code'].apply(lambda x: str('<a href="http://m.10jqka.com.cn/stockpage/hs_' + x + '">' + x + '</a>'))
    rtdf_html = HTML_with_style(rtdf)
    html_content += rtdf_html

    # 2.up-and-down price of recent 1 year
    if uad == True:
        html_content += '<h4>2.up-and-down price of recent 1 year:</h4>'
        wavedf = period.get_wave(codes, start='2017-01-01')
        wavedf = wavedf.replace(stkdict)
        # wavedf_html = wavedf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        wavedf_html = HTML_with_style(wavedf)
        html_content += wavedf_html

    # 3.moving average prices of several crucial periods
    if ma == True:
        html_content += '<h4>3.moving average prices of several crucial periods:</h4>'
        madf = maup.get_ma(codes, start='2017-01-01')
        # madf_html = madf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        madf_html = HTML_with_style(madf)
        html_content += madf_html

    # 4.limit-up of recent 1 year
    if lup == True:
        html_content += '<h4>4.limit-up of recent 1 year:</h4>'
        limitupdf = limitup.get_limit_up(codes, start='2017-01-01')
        limitupdf = limitupdf.replace(stkdict)
        # limitupdf_html = limitupdf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        limitupdf_html = HTML_with_style(limitupdf)
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


def create_attach(file=None, attchname=None):
    attach = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename=' + attchname
    return attach


def mail_with_attch(to_users=[], subject=None, content=None, attaches=[]):
    ret = True
    message = MIMEMultipart()
    message['From'] = formataddr(["FromRunoob", sender])
    # message['To'] = Header("test to", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(content, 'html', 'utf-8'))

    for i in range(0, len(attaches)):
        message.attach(attaches[i])

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  #SMTP server and port
        server.login(sender, passw)
        server.sendmail(sender, to_users, message.as_string())
        server.quit()  # close connection
    except Exception:
        ret = False
    return ret


if __name__ == '__main__':
    content1 = generate_report(title='The position stocks report', filename='ot', uad=True, ma=True, lup=True)
    _utils.save_to_pdf(content1, 'report_ot.pdf')
    content2 = generate_report(title='The tracking stocks report', monitor=True, filename='app/monitorot.txt', uad=True, ma=True, lup=True)
    _utils.save_to_pdf(content2, 'report_ot_trace.pdf')

    exit(0)
    attaches = []
    att1 = create_attach('otreport.pdf', 'daily_report.pdf')
    att2 = create_attach('trace_report.pdf', 'trace_report.pdf')
    attaches.append(att1)
    attaches.append(att2)
    # contenta = generate_report(title='The position stocks report', filename='pa', uad=True, ma=True, lup=True)
    # contentb = generate_report(title='The tracking stocks report', monitor=True, filename='app/monitormy.txt', uad=True, ma=True, lup=True)
    subj = "Stocks Report " + todaystr
    to_users = ['649054380@qq.com']#, '1677258052@qq.com', '53985188@qq.com']
    ret = mail_with_attch(to_users, subject=subj, content=content1+content2, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")