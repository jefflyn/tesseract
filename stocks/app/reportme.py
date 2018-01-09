from stocks.app import report
from stocks.app import _utils
from stocks.data import _datautils
from stocks.gene import maup
from stocks.gene import upnday
from stocks.etl import _reference

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
    att3 = report.create_attach('pa.png', 'position.png')
    attaches.append(att3)
    att4 = report.create_attach('trace.png', 'trace.png')
    attaches.append(att4)
    #attaches = generate_all(attaches)

    subj = "My Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content1+content2, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")

def generate_all(attaches):
    #maup
    basics = _datautils.get_basics(excludeCyb=True)
    codes = basics['code'].values
    maupdata = maup.get_ma(codes)
    maupdf = maup.get_ma_up(maupdata)
    # mauphtml = report.HTML_with_style(maupdf)
    # _utils.save_to_pdf(mauphtml, 'report_maup.pdf')
    # att3 = report.create_attach('report_maup.pdf', 'report_maup.pdf')
    maupdf.to_csv('report_maup.csv', encoding='utf-8')
    att3 = report.create_attach('report_maup.csv', 'report_maup.csv')
    attaches.append(att3)

    #upnday
    nupdf = upnday.get_upnday(codes)
    # nupdfhtml = report.HTML_with_style(nupdf)
    # _utils.save_to_pdf(nupdfhtml, 'report_upnday.pdf')
    # att4 = report.create_attach('report_upnday.pdf', 'report_upnday.pdf')
    nupdf.to_csv('report_upnday.csv', encoding='utf-8')
    att4 = report.create_attach('report_upnday.csv', 'report_upnday.csv')
    attaches.append(att4)

    #forcast
    forecast = _reference.get_forecast(2017, 4, afterdate='2017-12-01')
    forecast.to_csv('report_forecast.csv', encoding='utf-8')
    att5 = report.create_attach('report_forecast.csv', 'report_forecast.csv')
    attaches.append(att5)

    return attaches