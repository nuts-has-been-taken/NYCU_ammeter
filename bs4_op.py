import requests
from bs4 import BeautifulSoup
import os

def get_balance(t):

    url = "http://59.127.49.50/"

    body = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "ctl00$Content$BootstrapFormLayout1$edRoomNo": os.getenv('ROOM_NO'),
        "ctl00$Content$BootstrapFormLayout1$edPhone": os.getenv('PHONE'),
        "ctl00$Content$BootstrapFormLayout1$btnQuery": "查詢",
        "ctl00$Content$BootstrapFormLayout1$edQueryTime": t,
        "DXScript": "1_11,1_64,1_12,1_252,1_13,1_14,1_15,1_60,23_0,23_1,23_32,1_183,1_184,23_30,1_23,1_182,23_31",
        "DXCss": "23_80,23_88"
    }

    response = requests.post(url=url, data=body)

    #讀取金額
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        balance = soup.find('input', {'id': 'Content_BootstrapFormLayout1_edBalance_I'}).get("value")
        return True, balance
    else:
        return False, None