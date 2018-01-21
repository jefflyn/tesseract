from stocks.app import report
from stocks.app import _utils
from stocks.data import _datautils
from stocks.data import _reference
from stocks.gene import maup
from stocks.gene import upnday


if __name__ == '__main__':
    content = """  <html>  <head>  <meta name="pdfkit-page-size" content="Legal"/>  <meta name="pdfkit-orientation" content="Landscape"/> </head><body>"""
    content1 = report.generate_report2(title='Holding stocks report - pa', filename='pa')
    content12 = report.generate_report2(title='Holding stocks report - cf', filename='cf')
    content2 = report.generate_report2(title='Tracking stocks report', monitor=True, filename='app/monitormy.txt')
    content = content + content1 + content12 + content2 + '</body></html>'

    _utils.save_to_pdf(content, 'report_my.pdf')

    attaches = []
    att1 = report.create_attach('report_my.pdf', 'daily_report.pdf')
    attaches.append(att1)
    att0 = report.create_attach('wave_index.png', 'index.png')
    attaches.append(att0)
    att3 = report.create_attach('report_pa.png', 'holding-pa.png')
    attaches.append(att3)
    att31 = report.create_attach('report_cf.png', 'holding-cf.png')
    attaches.append(att31)
    att4 = report.create_attach('report_trace.png', 'trace.png')
    attaches.append(att4)
    #attaches = generate_all(attaches)

    subj = "My Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
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