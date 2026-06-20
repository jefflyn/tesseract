import os
import smtplib

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

sender = 'jefflyn0321@qq.com'
sender_alias = '咕噜咕噜魔法阵'
passw = 'bmoikagqczlpbbhb'


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


def send_mobile_friendly_email(to_users=[], subject=None, title=None, data=None, columns=None):
    '''
    Send mobile-friendly HTML email with table data
    :param to_users: List of recipient email addresses
    :param subject: Email subject
    :param title: Table title displayed in email
    :param data: List of dictionaries containing table data
    :param columns: List of column configurations [{'key': 'field_name', 'label': 'Display Name'}]
    :return: True if sent successfully, False otherwise
    '''
    ret = True

    # Build responsive HTML content optimized for mobile
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 10px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 20px;
            font-weight: 600;
        }}
        .content {{
            padding: 15px;
        }}
        .table-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin-top: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 400px;
        }}
        th {{
            background-color: #f8f9fa;
            color: #333;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            border-bottom: 2px solid #dee2e6;
            white-space: nowrap;
        }}
        td {{
            padding: 10px 8px;
            border-bottom: 1px solid #dee2e6;
            font-size: 13px;
            color: #555;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e9ecef;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
        }}
        @media screen and (max-width: 480px) {{
            body {{
                padding: 5px;
            }}
            .header {{
                padding: 15px;
            }}
            .header h1 {{
                font-size: 18px;
            }}
            .content {{
                padding: 10px;
            }}
            th, td {{
                padding: 8px 6px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title or subject}</h1>
        </div>
        <div class="content">
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
'''

    # Add column headers
    if columns and data:
        for col in columns:
            html_content += f'                            <th>{col["label"]}</th>\n'

        html_content += '''                        </tr>
                    </thead>
                    <tbody>
'''

        # Add data rows
        for row in data:
            html_content += '                        <tr>\n'
            for col in columns:
                value = row.get(col['key'], '')
                # Format value based on type
                if value is None:
                    value = '-'
                elif isinstance(value, float):
                    value = f'{value:.2f}'
                html_content += f'                            <td>{value}</td>\n'
            html_content += '                        </tr>\n'

        html_content += '''                    </tbody>
                </table>
            </div>
        </div>
        <div class="footer">
            <p>此邮件由系统自动发送，请勿直接回复</p>
        </div>
    </div>
</body>
</html>'''
    else:
        # Fallback for no data
        html_content += '''
            <div class="content">
                <p style="text-align: center; color: #6c757d;">暂无数据</p>
            </div>
        </div>
        <div class="footer">
            <p>此邮件由系统自动发送，请勿直接回复</p>
        </div>
    </div>
</body>
</html>'''

    # Send email
    try:
        message = MIMEMultipart()
        message['From'] = formataddr([sender_alias, sender])
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(html_content, 'html', 'utf-8'))

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, passw)
        server.sendmail(sender, to_users, message.as_string())
        server.quit()
    except Exception as e:
        import traceback
        print(f"❌ 邮件发送失败: {str(e)}")
        print(f"错误详情:\n{traceback.format_exc()}")
        ret = False

    return ret
