from stocks.app import report
from stocks.app import _utils


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
    content = report.generate_report(title='The tracking stocks report', monitor=True, filename='app/zl.txt', uad=True, ma=True, lup=True)
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
    content1 = report.generate_report(title='The position stocks report', filename='ot', uad=True, ma=True, lup=True)
    content2 = report.generate_report(title='The tracking stocks report', monitor=True, filename='app/monitorot.txt',
                                      uad=True, ma=True, lup=True)
    _utils.save_to_pdf(content1 + content2, 'report_ot.pdf')

    attaches = []
    # att0 = report.create_attach('wave_index.png', 'index.png')
    # attaches.append(att0)

    att1 = report.create_attach('report_ot.pdf', 'daily_report.pdf')
    attaches.append(att1)

    att2 = report.create_attach('report_ot.png', 'position.png')
    attaches.append(att2)
    att3 = report.create_attach('report_trace.png', 'trace.png')
    attaches.append(att3)

    subj = "Your Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com', '1677258052@qq.com', '53985188@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content1 + content2, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")

if __name__ == '__main__':
    # report_to_zl()
    report_to_kk()