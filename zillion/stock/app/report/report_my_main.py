from datetime import datetime

from zillion.stock.app import report
from zillion.stock.app.selection import selector
from zillion.stock.data import data_util

if __name__ == '__main__':
    content = """  <html>  <head>  <meta name="pdfkit-page-size" content="Legal"/>  <meta name="pdfkit-orientation" content="Landscape"/> </head><body>"""
    content1 = report.generate_report2(title='pa', filename='pa')
    content2 = report.generate_report2(title='cf', filename='cf')
    # content2 = report.generate_report2(title='Tracking zillion report', monitor=True, filename='app/monitormy.txt')
    content = content + content1 + content2 + '</body></html>'
    # content = content + content12 + '</body></html>'

    selector.select_result(data_util.get_app_codes(), filename='my')

    attaches = []
    att1 = report.create_attach('select_result_my.csv', 'select_result_my.csv')
    attaches.append(att1)
    att0 = report.create_attach('wave_index.png', 'index.png')
    attaches.append(att0)
    att3 = report.create_attach('report_pa.png', 'holding-pa.png')
    attaches.append(att3)
    att31 = report.create_attach('report_cf.png', 'holding-cf.png')
    attaches.append(att31)
    # att4 = report.create_attach('report_trace.png', 'trace.png')
    # attaches.append(att4)
    #attaches = generate_all(attaches)

    subj = "My Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        todaystr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Email send successfully. " + todaystr)
    else:
        print("Send failed")
