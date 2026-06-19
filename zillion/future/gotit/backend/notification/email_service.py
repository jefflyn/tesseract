"""
Email Notification Service
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List
import os
from datetime import datetime


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.qq.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')

    def send_notification(self, subject: str, content: str, recipients: List[str]):
        """Send email notification"""
        if not self.sender_email or not self.sender_password:
            print("Email configuration not set. Skipping notification.")
            return

        try:
            message = MIMEMultipart()
            message['From'] = Header(f'Futures System <{self.sender_email}>')
            message['To'] = Header(', '.join(recipients))
            message['Subject'] = Header(subject, 'utf-8')

            message.attach(MIMEText(content, 'html', 'utf-8'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipients, message.as_string())
            server.quit()

            print(f"Email sent successfully to {recipients}")

        except Exception as e:
            print(f"Error sending email: {e}")
            raise

    def send_daily_report(self, update_results: List[dict], recipients: List[str]):
        """Send daily update report"""
        subject = "期货数据每日更新报告"

        content = "<h2>期货数据每日更新报告</h2>"
        content += f"<p>更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        content += "<table border='1' cellpadding='5' cellspacing='0'>"
        content += "<tr><th>合约</th><th>更新记录数</th><th>状态</th></tr>"

        for result in update_results:
            status = "成功" if 'records' in result else "失败"
            records = result.get('records', 0)
            content += f"<tr><td>{result['contract']}</td><td>{records}</td><td>{status}</td></tr>"

        content += "</table>"

        self.send_notification(subject, content, recipients)


email_service = EmailService()
