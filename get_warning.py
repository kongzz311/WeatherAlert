import os
import requests


def get_warning(location):
    LOCATION = location
    KEY = os.environ.get('WEATHER_API')

    URL = 'https://devapi.qweather.com/v7/warning/now'

    params = {
        'key': KEY,
        'location': LOCATION
    }

    response_ = requests.get(URL, params=params)

    print(response_.json())

    response = response_.json()


    if response['code'] == '200':
        if response['warning']:
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

            # send_mail(title, body)

            return id, title, body
        else:
            return None, None, None


if __name__ == '__main__':
    get_warning('101221701')