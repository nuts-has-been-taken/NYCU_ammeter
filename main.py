import sheet_op
import bs4_op
import line_op
import datetime
from dotenv import load_dotenv

def main():

    load_dotenv()

    t = datetime.datetime.now().strftime("%Y-%m-%d")
    res, balance = bs4_op.get_balance(t)

    if res:
        #紀錄到excel (不需要使用到資料庫)
        try:
            res, t_before, cost = sheet_op.workbook_save(t, balance)
        except Exception as e:
            line_op.send(status="excel_false", text=f"儲存至 excel 時出現了問題，如果可以請檢查錯誤\nmsg error : {e}")
            return
        line_op.send(status=res, t_before=t_before, t_now=t, cost=cost, balance=balance)
    else:
        line_op.send(status="bs4_false", text="在取得餘額時出了點問題，請直接使用瀏覽器確認 http://59.127.49.50/")


if __name__ == "__main__":
    main()