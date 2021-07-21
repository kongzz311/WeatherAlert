import smtplib
import os
import json
import configparser
import requests
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class Email:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.cfg')

        self.EMAIL_ADDRESS = config['EMAIL']['SEND_EMAIL_ADDRESS']
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        self.SMTP_SERVER = config['EMAIL']['SMTP_SERVER']
        self.SMTP_SERVER_PORT = config['EMAIL']['SMTP_SERVER_PORT']
        self.RECEIVERS = config['EMAIL']['RECEIVER'].split(',')
        print(self.RECEIVERS)

    def send_mail(self, subject, body):
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = _format_addr('天气灾害预警 <%s>' % self.EMAIL_ADDRESS)
        msg['To'] = _format_addr('<%s>' % self.RECEIVERS)
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_SERVER_PORT)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

        server.sendmail(self.EMAIL_ADDRESS, self.RECEIVERS, msg.as_string())
        server.quit()

if __name__ == '__main__':
    email = Email()
    email.send_mail('test', 'test')