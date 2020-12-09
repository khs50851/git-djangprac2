import requests
import datetime


def get_exchange():
    today = datetime.datetime.now()
    if today.weekday() >= 5:
        diff = today.weekday()-4
        today = today - datetime.timedelta(day=diff)

    today = today.strftime('%Y%m%d')
    auth = 'znMghnw9jskYa3P6ovLYk77qRdX4v2gb'
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={}&searchdate={}&data=AP01'
    url = url.format(auth, today)
    res = requests.get(url)
    data = res.json()

    for d in data:
        if d['cur_unit'] == 'USD':  # 통화 유닛을 달러로
            return d['tts']  # 보낼때 환율
    return
