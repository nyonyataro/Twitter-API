import datetime, os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

# 設定
json_file = os.getenv('JSON_FILE')
file_name = 'Twitter_Users'
sheet_name1 = 'シート1'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
# スプレッドシートにアクセス
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file, scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)
SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')

wb = gc.open_by_key(SPREADSHEET_KEY)
ws = wb.sheet1

def append_users(users):
    ws.append_row(users)

def judge_user_existence(user):
    return ws.find(user)

#スプレッドシートの「フォローされているか」の列を埋めて、片思いの人を返す
def check_am_i_followed():
    from app import follower_id
    #スプシの2行目以降
    follow_id = ws.col_values(2)[1:]
    kataomoi_ids = list(set(follow_id) - (set(follower_id) & set(follow_id)))
    
    #○と×の列
    followed_or_not_list = ws.col_values(4)[1:]
    id_list = ws.col_values(2)[1:]
    delete_row_list = []
    for i, (id_cell, followed_or_not) in enumerate(zip(id_list, followed_or_not_list)):
        if followed_or_not == '○':
            print('○なので削除します')
            delete_row_list.append(i+2)
        elif id_cell in follower_id:
            print(f'両思いなので{id_cell}を削除します')
            delete_row_list.append(i+2)
            # ws.update_cell(i+2, 4, "○")
        else:
            print(f'片思いなので{id_cell}を×のままにする')
            # ws.update_cell(i+2, 4, "×")
    print(delete_row_list)
    #使い終わった行を削除
    for i, delete_row in enumerate(delete_row_list):
        delete_row = delete_row - i
        ws.delete_rows(delete_row)
    return kataomoi_ids

def return_unfollow_ids():
    unfollow_ids = []
    dt_now = datetime.datetime.now()
    i = 0
    while ws.cell(i+2, 3).value:
        follow_date = datetime.datetime.strptime(ws.cell(i+2, 3).value, '%Y-%m-%d')
        dt_delta = dt_now - follow_date
        if dt_delta.days >= 2:
            unfollow_ids.append(ws.cell(i+2,2).value)
            #フォロー返さない人を消す
            ws.delete_row(i+2)
        i += 1
    return unfollow_ids

# check_am_i_followed()
# return_unfollow_ids()