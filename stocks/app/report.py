import datetime
import os
import re
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import numpy as np
import pandas as pd
from stocks.app import realtime
from stocks.data import data_util
from stocks.gene import limitup
from stocks.gene import maup
from stocks.gene import wave
import stocks.util.db_util as _dt



sender = '649054380@qq.com'
passw = 'pznntikuyzfvbchb'
# to_users = '649054380@qq.com'
# to_users = ['649054380@qq.com', '1677258052@qq.com','53985188@qq.com']

todaystr = datetime.datetime.now().strftime('%Y-%m-%d')


def get_limitup_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low) / low * 100


def get_warn_space(df):
    price = float(df[0])
    low = float(df[1])
    return (price - low)


"""
return result with html style
"""


def generate_report2(title=None, filename=None, monitor=False):
    # 1.realtime info
    html_content = '<i>' + title + '</i>'
    savefilename = 'report_' + filename + '.png'
    rtdf = None
    if monitor == False:
        rtdf = realtime.get_realtime(filename, sortby='b')
        rtdf = rtdf[
            ['warn', 'code', 'name', 'price', 'change', 'low', 'wave', 'bottom', 'uspace', 'cost', 'profit_amt',
             'profit_perc', 'total_amt']]
        rtdf.rename(
            columns={'uspace': 'space', 'profit_amt': 'profit', 'profit_perc': 'percent', 'total_amt': 'amount'},
            inplace=True)
    else:
        savefilename = 'report_trace.png'
        df = data_util.get_data('../data/' + filename, sep=' ')
        codes = list(df['code'])
        rtdf = falco.get_monitor(codes)
        rtdf = rtdf[['warn', 'code', 'name', 'change', 'price', 'low', 'bottom', 'space', 'industry', 'area', 'pe']]

    rtdf = rtdf.sort_values('space', ascending=False)
    codes = list(rtdf.code)
    names = list(rtdf.name)
    stkdict = dict(zip(codes, names))
    codes.reverse()

    # moving average prices of several crucial waves
    madf = maup.get_ma_data(codes, start='2017-01-01')

    # limit-up of recent half year
    limitupdf = limitup.get_limitup_from_hist_k(codes, start='2017-01-01')
    limitupcount = limitup.count(limitupdf)

    result = pd.merge(rtdf, madf[['code', 'isup', 'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma10_space']],
                      on='code', how='left')
    result = pd.merge(result, limitupcount[['code', 'count', 'mindate', 'maxdate', 'lup_low']],
                      on='code', how='left')
    result['lmtspace'] = result[['price', 'lup_low']].apply(get_limitup_space, axis=1)
    # result['warn'] = result[['lmtspace', 'space']].apply(get_warn_space, axis=1)
    # result['warn'] = result['warn'].apply(lambda x: str(round(x, 2)) + '%')
    # result['change'] = result['change'].apply(lambda x: str(round(x, 2)) + '%')
    result['space'] = result['space'].apply(lambda x: str(round(x, 2)) + '%')
    result['ma10_space'] = result['ma10_space'].apply(lambda x: str(round(x, 2)) + '%')
    result['lmtspace'] = result['lmtspace'].apply(lambda x: str(round(x, 2)) + '%')

    # style format
    # rtdf['code'] = rtdf['code'].apply(lambda x: str('<a href="http://m.10jqka.com.cn/stockpage/hs_' + x + '">' + x + '</a>'))
    rtdf_html = HTML_with_style(result)
    html_content += rtdf_html

    # up-and-down price of recent 1 year
    wavedf = wave.get_wave(codes, start='2016-01-01')
    # plot figure
    listdf = []
    for code in codes:
        wdf = wavedf[wavedf.code == code]
        wave_format = wave.format_wave_data(wdf)
        if wave_format is None:
            continue
        listdf.append(wave_format)
    # figure display
    wave.plot_wave(listdf, filename=savefilename)

    wavedf = wavedf.replace(stkdict)

    return html_content


def HTML_with_style(df, style=None, random_id=None):
    df_html = df.to_html(index=False, index_names=False)

    if random_id is None:
        random_id = 'id%d' % np.random.choice(np.arange(1000000))

    if style is None:
        style = """
        <style>
            table#{random_id} {{border-collapse:collapse; border-width: 1px; border-style: solid; border-color: rgb(235, 242, 224);}}
            table#{random_id} thead, table#{random_id} tr {{border-top-width: 1px; text-align:right;}}
            table#{random_id} td, table#{random_id} th {{word-break: keep-all; padding: 5px 10px; font-size: 14px; font-family: Verdana;}}
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

    savefilename = 'report_' + filename + '.png'
    rtdf = None
    if monitor == False:
        rtdf = realtime.get_realtime(filename, sortby='b')
        rtdf = rtdf[
            ['warn', 'code', 'name', 'price', 'change', 'low', 'bottom', 'btm_space', 'cost', 'profit_amt',
             'profit_perc', 'total_amt']]
        # rtdf.columns = ['a', 'b', 'c']
        rtdf.rename(
            columns={'btm_space': 'space', 'profit_amt': 'profit', 'profit_perc': 'percent', 'total_amt': 'amount'},
            inplace=True)
    else:
        savefilename = 'report_trace.png'
        df = data_util.get_data('../data/' + filename, sep=' ')
        codes = list(df['code'])
        rtdf = falco.get_monitor(codes)
        rtdf = rtdf[['warn', 'code', 'name', 'change', 'price', 'low', 'bottom', 'space', 'industry', 'area', 'pe']]

        rtdf['change'] = rtdf['change'].apply(lambda n: str(round(n, 3)) + '%')
        rtdf['space'] = rtdf['space'].apply(lambda n: str(round(n, 3)) + '%')
    # rtdf = rtdf.sort_values('space', ascending=False)
    codes = list(rtdf.code)
    names = list(rtdf.name)
    stkdict = dict(zip(codes, names))
    codes.reverse()

    # style format
    # rtdf['code'] = rtdf['code'].apply(lambda x: str('<a href="http://m.10jqka.com.cn/stockpage/hs_' + x + '">' + x + '</a>'))
    rtdf_html = HTML_with_style(rtdf)
    html_content += rtdf_html

    # 2.up-and-down price of recent 1 year
    if uad == True:
        html_content += '<h4>2.up-and-down price of recent 1 year:</h4>'
        wavedf = wave.get_wave(codes, start='2016-01-01')
        # plot figure
        listdf = []
        for code in codes:
            wdf = wavedf[wavedf.code == code]
            listdf.append(wave.format_wave_data(wdf))
        # figure display
        wave.plot_wave(listdf, filename=savefilename)

        wavedf = wavedf.replace(stkdict)
        # wavedf_html = wavedf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        wavedf_html = HTML_with_style(wavedf)
        html_content += wavedf_html

    # 3.moving average prices of several crucial waves
    if ma is True:
        html_content += '<h4>3.moving average prices of several crucial waves:</h4>'
        madf = maup.get_ma_data(codes, start='2017-01-01')
        # madf_html = madf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        madf_html = HTML_with_style(madf)
        html_content += madf_html

    # 4.limit-up of recent 1 year
    if lup is True:
        html_content += '<h4>4.limit-up of recent 1 year:</h4>'
        limitupdf = limitup.get_limitup_from_hist_k(codes, start='2017-01-01')
        limitupdf = limitupdf.replace(stkdict)
        # limitupdf_html = limitupdf.to_html(escape=False, index=False, sparsify=True, border=0, index_names=False, header=True)
        limitupdf_html = HTML_with_style(limitupdf)
        html_content += limitupdf_html

    return html_content


def mail(to_users=[], content=None):
    ret = True
    try:
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr(["Jefflyn", sender])  # sender nickname and account
        # msg['To'] = formataddr(["FK", to_users])  # receiver nickname and account
        msg['Subject'] = todaystr + " Stocks Report"  # subject

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP server and port
        server.login(sender, passw)
        server.sendmail(sender, to_users, msg.as_string())
        server.quit()  # close connection
    except Exception as e:
        print(str(e))
        ret = False
    return ret


def create_attach(file=None, attchname=None):
    attchfile = open(file, 'rb')
    filename = os.path.basename(attchfile.name)
    attchname = filename if attchname is None else attchname
    attach = MIMEText(attchfile.read(), 'base64', 'utf-8')
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename=' + attchname
    return attach


def mail_with_attch(to_users=[], subject=None, content=None, attaches=[]):
    ret = True
    message = MIMEMultipart()
    message['From'] = formataddr(["jefflyn", sender])
    # message['To'] = Header("test to", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(content, 'html', 'utf-8'))

    for i in range(0, len(attaches)):
        message.attach(attaches[i])

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP server and port
        server.login(sender, passw)
        server.sendmail(sender, to_users, message.as_string())
        server.quit()  # close connection
    except Exception:
        ret = False
    return ret


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
    att = create_attach(file='select.xlsx')
    attaches.append(att)

    subj = "Stock Selection Report " + todaystr
    to_users = ['649054380@qq.com']
    ret = mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")

