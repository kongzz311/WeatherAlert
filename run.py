import schedule
import time
import configparser
import datetime
from send_mail import Email
from get_warning import get_warning


config = configparser.ConfigParser()
config.read('./config.cfg')
locations = config['API']['LOCATIONS'].split(',')
last_warning_ids = []
for location in locations:
    last_warning_ids.append(None)

def job():
    id, title, body = None, None, None
    global last_warning_ids, locations
    for idx, location in enumerate(locations):
        try:
            id, title, body = get_warning(location)
        except:
            print(datetime.datetime.now(),"获取信息失败")
        if id and id != last_warning_ids[idx]:
            try:
                email = Email()
                email.send_mail(title, body)
                last_warning_ids[idx] = id
            except:
                print(datetime.datetime.now(), "发送失败")
    print(datetime.datetime.now(), last_warning_ids)

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
