from stocks.app import report

if __name__ == '__main__':
    content = """  <html>  <head>  <meta name="pdfkit-page-size" content="Legal"/>  <meta name="pdfkit-orientation" content="Landscape"/> </head><body>"""
    data = report.generate_report2(title='Tracking stocks report', monitor=True, filename='app/sz50.txt')
    content = content + data + '</body></html>'

    # _utils.save_to_pdf(content, 'report_my.pdf')
    attaches = []
    # att1 = report.create_attach('report_my.pdf', 'daily_report.pdf')
    # attaches.append(att1)

    att = report.create_attach('report_trace.png', 'report_sz50.png')
    attaches.append(att)
    #attaches = generate_all(attaches)

    subj = "My Stocks Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")
