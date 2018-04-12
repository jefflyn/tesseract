from stocks.app import index
from stocks.app import report
from stocks.app import selector
from stocks.data import _datautils
from stocks.data.concept import constants as CCONTS
from stocks.data.industry import constants as ICONTS

if __name__ == '__main__':
    content = 'Please find the attaches for the selection report details.'
    # index.get_status()
    # selector.select_xxx('app')
    # selector.select_concepts(CCONTS.JYYC, 'jyyc')
    # selector.select_concepts(CCONTS.RGZN, 'rgzn')
    # selector.select_industry(ICONTS.JSJYY, 'jsjyy')
    # selector.select_subnew()
    codes = _datautils.get_app_codes()
    selector.select_result(codes, 'app')

    codes = _datautils.get_monitor_codes()
    selector.select_result(codes, 'monitor')

    attaches = []
    att1 = report.create_attach('select_result_app.csv')
    attaches.append(att1)
    att2 = report.create_attach('select_result_monitor.csv')
    attaches.append(att2)
    # att3 = report.create_attach('select_jsjyy.csv')
    # attaches.append(att3)

    subj = "Stock Selection Report " + report.todaystr
    to_users = ['649054380@qq.com']
    ret = report.mail_with_attch(to_users, subject=subj, content=content, attaches=attaches)
    if ret:
        print("Email send successfully")
    else:
        print("Send failed")
