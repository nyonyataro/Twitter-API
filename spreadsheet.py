import datetime, os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
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
# df = pd.DataFrame(ws.get_all_values()[1:], columns=ws.get_all_values()[0])

def append_users(users):
    ws.append_row(users)

def judge_user_existence(user):
    return ws.find(user)

#スプレッドシートの「フォローされているか」の列を埋めて、片思いの人を返す
def check_am_i_followed():
    from app import follower_id
    #followerのidをstrに

    #スプシの2行目以降
    follow_id :list[str] = ws.col_values(2)[1:]
    kataomoi_ids : list[str] = list(set(follow_id) - (set(follower_id) & set(follow_id)))

    df = pd.DataFrame(ws.get_all_values()[1:], columns=ws.get_all_values()[0])
    df_remain = df[df.iloc[:, 1].isin(kataomoi_ids)]
    df_delete = df[~(df.iloc[:, 1].isin(kataomoi_ids))]['id']
    
    ws.clear()
    set_with_dataframe(ws, df_remain, include_column_header=True)
    print(f'両思いになった人たち{ df_delete }')


    # #○と×の列
    # followed_or_not_list = ws.col_values(4)[1:]
    # id_list = ws.col_values(2)[1:]
    # delete_row_list = []
    # for i, (id_cell, followed_or_not) in enumerate(zip(id_list, followed_or_not_list)):
    #     if followed_or_not == '○':
    #         print('○なので削除します')
    #         delete_row_list.append(i+2)
    #     elif id_cell in follower_id:
    #         print(f'両思いなので{id_cell}を削除します')
    #         delete_row_list.append(i+2)
    #         # ws.update_cell(i+2, 4, "○")
    #     else:
    #         print(f'片思いなので{id_cell}を×のままにする')
    #         # ws.update_cell(i+2, 4, "×")
    # print(f'右の行のユーザーをスプシから削除します:{delete_row_list}')
    # #使い終わった行を削除
    # for i, delete_row in enumerate(delete_row_list):
    #     delete_row = delete_row - i
    #     ws.delete_rows(delete_row)
    return kataomoi_ids

def return_unfollow_ids():
    df = pd.DataFrame(ws.get_all_values()[1:], columns=ws.get_all_values()[0])
    dt_now = pd.to_datetime(datetime.datetime.now())
    df['フォロー日'] = pd.to_datetime(df['フォロー日'])
    df_remain = df[(dt_now - df['フォロー日']) / datetime.timedelta(days=1) <= 2]
    df_delete = df[(dt_now - df['フォロー日']) / datetime.timedelta(days=1) > 2]
    df_delete = df_delete.iloc[:,1].to_list()
    ws.clear()
    set_with_dataframe(ws, df_remain, include_column_header=True)
    print(df_delete)
    return df_delete