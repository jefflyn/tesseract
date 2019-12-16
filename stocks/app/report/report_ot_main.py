from datetime import datetime

from stocks.util import _utils
from stocks.app import report
from stocks.app import selector
from stocks.data import data_util



def report_to_zl():
    """
    601668
    002415
    601111
    600477

    601988
    601006
    601328
    601186
    600690
    000069
    601398
    600028
    600036
    600153
    601939
    600018
    :return:
    """
    content = report.generate_report(title='The tracking stocks report', monitor=True, filename='app/zl.txt', uad=True,
                                     ma=True, lup=True)
    _utils.save_to_pdf(content, 'report_zl.pdf')

    attaches = []

    att1 = report.create_attach('report_zl.pdf', 'daily_report.pdf')
    attaches.append(att1)

    att2 = report.create_attach('report_trace.png', 'position.png')
    attaches.append(att2)

    subj = "Your Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com', '251537147@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")


def report_to_kk():
    content = """  <html>  <head>  <meta name="pdfkit-page-size" content="Legal"/>  <meta name="pdfkit-orientation" content="Landscape"/> </head><body>"""
    content1 = 'Please check the attaches for more details.'
    content = content + content1 + '</body></html>'

    selector.select_result(data_util.get_monitor_codes('ot'), 'ot')

    attaches = []
    att1 = report.create_attach('select_result_ot.csv', 'select_result_ot.csv')
    attaches.append(att1)
    att2 = report.create_attach('wave_index.png', 'index.png')
    attaches.append(att2)
    att3 = report.create_attach('index_status.csv', 'index_status.csv')
    attaches.append(att3)

    subj = "Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com', '1677258052@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        todaystr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Email send successfully. " + todaystr)
    else:
        print("Send failed")


if __name__ == '__main__':
    # report_to_zl()
    report_to_kk()
