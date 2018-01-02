from stocks.app import report
from stocks.app import _utils
from stocks.data import _datautils
from stocks.gene import maup
from stocks.gene import upnday

if __name__ == '__main__':
    content1 = report.generate_report(title='The position stocks report', filename='pa', uad=True, ma=True, lup=True)
    _utils.save_to_pdf(content1, 'report_my.pdf')

    content2 = report.generate_report(title='The tracking stocks report', monitor=True, filename='app/monitormy.txt', uad=True, ma=True, lup=True)
    _utils.save_to_pdf(content2, 'report_my_trace.pdf')
    attaches = []
    att1 = report.create_attach('report_my.pdf', 'daily_report.pdf')
    att2 = report.create_attach('report_my_trace.pdf', 'trace_report.pdf')
    attaches.append(att1)
    attaches.append(att2)

    #maup
    basics = _datautils.get_basics(excludeCyb=True)
    codes = basics['code'].values
    maupdata = maup.get_ma(codes)
    maupdf = maup.get_ma_up(maupdata)

    #upnday
    nupdf = upnday.get_upnday(codes)

    _utils.save_to_pdf(maupdf, 'report_maup.pdf')
    _utils.save_to_pdf(nupdf, 'report_upnday.pdf')

    att3 = report.create_attach('report_maup.pdf', 'report_maup.pdf')
    att4 = report.create_attach('report_upnday.pdf', 'report_upnday.pdf')
    attaches.append(att3)
    attaches.append(att4)

    subj = report.todaystr + " Stocks Report"
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content1+content2, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")