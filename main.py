import smtplib
import os
import configparser
import requests
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

config = configparser.ConfigParser()
config.read('./config.cfg')
LOCATION = config['API']['LOCATION']
KEY = config['API']['KEY']

EMAIL_ADDRESS = config['EMAIL']['SEND_EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
SMTP_SERVER = config['EMAIL']['SMTP_SERVER']
SMTP_SERVER_PORT = config['EMAIL']['SMTP_SERVER_PORT']
RECEIVER = config['EMAIL']['RECEIVER']

print(SMTP_SERVER, SMTP_SERVER_PORT)

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = _format_addr('天气灾害预警 <%s>' % EMAIL_ADDRESS)
    msg['To'] = _format_addr('<%s>' % RECEIVER)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, [RECEIVER], msg.as_string())
    server.quit()



URL = 'https://devapi.qweather.com/v7/warning/now'

params = {
    'key': KEY,
    'location': LOCATION
}

response_ = requests.get(URL, params=params)

print(response_.json())

response = response_.json()

last_warning_id = ''

if response['code'] == '200':
    if response['warning']:
        if response['warning'][0]['id'] != last_warning_id:
            id = response['warning'][0]['id']
            sender = response['warning'][0]['sender'] if 'sender' in response['warning'][0] else '未知'
            pubTime = response['warning'][0]['pubTime']
            title = response['warning'][0]['title']
            startTime = response['warning'][0]['startTime'] if 'startTime' in response['warning'][0] else '未知'
            endTime = response['warning'][0]['endTime'] if 'endTime' in response['warning'][0] else '未知'
            status = response['warning'][0]['status'] if 'status' in response['warning'][0] else '未知'
            level = response['warning'][0]['level']
            typeName = response['warning'][0]['typeName']
            text = response['warning'][0]['text']

            body = f"{text}\n\n发送者：{sender}\n发布时间：{pubTime}\n开始时间：{startTime}\n结束时间：{endTime}\n状态：{status}\n等级：{level}\n灾害类型：{typeName}\n"

            send_mail(title, body)

            response['warning'][0]['id'] = id

