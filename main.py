import os
import sys
import re
import requests
import datetime
from lxml.html import document_fromstring

def get_validatecode(session: requests.Session) -> str:
    import pytesseract
    from PIL import Image
    from io import BytesIO

    for attempts in range(20):
        response = session.get(
            "https://passport.ustc.edu.cn/validatecode.jsp?type=login"
        )
        stream = BytesIO(response.content)
        image = Image.open(stream)
        text = pytesseract.image_to_string(image)
        codes = re.findall(r"\d{4}", text)
        if len(codes) == 1:
            break
    return codes[0]


def login(session: requests.Session, username: str, password: str):
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Origin": "https://passport.ustc.edu.cn",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
        }
    )
    session.cookies.set("lang", "zh")
    response = session.get(
        "http://hs.lib.ustc.edu.cn/account/Login",
        headers={"Referer": "http://hs.lib.ustc.edu.cn/account/Login"},
    )
    CAS_LT= re.findall(r'LT-.*?\"', response.text)[0][:-1]
    response = session.post(
        "https://passport.ustc.edu.cn/login",
        data={
            "model": "uplogin.jsp",
            "CAS_LT": CAS_LT,
            "service": "http://hs.lib.ustc.edu.cn/account/Login",
            "warn": "",
            "showCode": "1",
            "qrCode": "",
            "resultInput": "",
            "username": username,
            "password": password,
            "LT": get_validatecode(session)
        },
        headers={
            "Referer": "https://passport.ustc.edu.cn/login?service=http://hs.lib.ustc.edu.cn/account/Login",
        },
        allow_redirects=True,
    )
    return session

def make_appointment(session: requests.Session, username: str, _: str):
    # get today in UTC+8 as "yyyy-mm-dd"
    date = datetime.datetime.now() + datetime.timedelta(hours=8)
    date += datetime.timedelta(days=3)
    date = date.strftime("%Y-%m-%d")
    print(date)
    response = session.post(
        "https://hs.lib.ustc.edu.cn/desktopAppointment/affirmAppointment",
        data={
            "resTypeID": 1,
            "PartionID": 38,
            "dateName": date,
            "startTime": "09:50",
            "endTime": "11:50",
            "userid": username,
            "theme": "【线上会议】",
            "otherAppointees": "",
            "resourceId": 875,
            "isChair": "false"
        },
    )


    return response


if __name__ == "__main__":
    IDENT = os.environ["IDENT"]
    session = requests.Session()
    session = login(session, *IDENT.split(":"))
    print("logined")
    r = make_appointment(session, *IDENT.split(":"))
    print(r.text)