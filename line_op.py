from datetime import datetime
import requests
import os

def send(status:str, t_before="", t_now="", cost=None, balance=None, text=""):
    if status=="success":
        success(t_before=t_before, t_now=t_now, cost=cost, balance=balance)
    elif status=="top_up":
        top_up(t_before=t_before, cost=cost, balance=balance)
    elif status=="start":
        start(balance=balance)
    else:
        fail(status=status, text=text)
    return

def success(t_before, t_now, cost, balance):
    date_now = datetime.strptime(t_now, "%Y-%m-%d")
    date_bef = datetime.strptime(t_before, "%Y-%m-%d")
    diff_days = (date_now - date_bef).days
    msg = "電費通知\n"
    cost = eval("{:.2f}".format(cost))
    if diff_days==1:
        msg += f"""你昨天花了 {cost} 元\n你的餘額還有 {balance} 元"""
    elif diff_days==0:
        return
    else:
        avg_cost = "{:.2f}".format(cost/diff_days)
        msg += f"""從 {t_before} 到現在一共花了 {cost} 元\n平均一天花了 {avg_cost} 元\n你的餘額還有 {balance} 元"""
    send_line_notify(msg)
    return

def top_up(t_before, cost, balance):
    date_bef = t_before.strftime("%Y-%m-%d")
    msg = "電費通知\n"
    msg += f"""你似乎儲值了，{date_bef} 時你還有 {cost} 元\n現在你的餘額是 {balance} 元"""
    send_line_notify(msg)
    return

def start(balance):
    msg = "電費通知\n"
    msg += f"""今天是開始紀錄的第一天，你的餘額還有 {balance} 元"""
    send_line_notify(msg)
    return

def fail(status:str, text:str):
    msg = "電費通知\n"
    msg += f"{status}\n錯誤:{text}"
    send_line_notify(msg)
    return
    
def send_line_notify(msg:str):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + os.getenv("LINE_NOTIFY_TOKEN")}
    payload = {"message": msg}
    r = requests.post(url, headers=headers, params=payload)
    return