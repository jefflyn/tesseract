import os
import smtplib

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '649054380@qq.com'
sender_alias = '【咕噜咕噜魔法阵】'
passw = 'pznntikuyzfvbchb'


def create_attach(file=None, attchname=None):
    '''
    添加附件
    :param file:
    :param attchname:
    :return:
    '''
    attchfile = open(file, 'rb')
    filename = os.path.basename(attchfile.name)
    attchname = filename if attchname is None else attchname
    attach = MIMEText(attchfile.read(), 'base64', 'utf-8')
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename=' + attchname
    return attach


def mail_with_attch(to_users=[], subject=None, content=None, attaches=[]):
    '''
    带附件发送邮件
    :param to_users:
    :param subject:
    :param content:
    :param attaches:
    :return:
    '''
    ret = True
    message = MIMEMultipart()
    message['From'] = formataddr([sender_alias, sender])
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


