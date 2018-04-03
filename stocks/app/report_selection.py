from stocks.app import index
from stocks.app import report
from stocks.app import selector

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'

    index.get_status()
    selector.select_subnew()

    attaches = []
    att1 = report.create_attach('index_status.csv')
    att2 = report.create_attach('select_result.csv')
    att3 = report.create_attach('select_wave.csv')
    attaches.append(att1)
    attaches.append(att2)
    attaches.append(att3)

    subj = "Stock Selection Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")
