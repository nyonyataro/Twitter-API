import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 設定
json_file = 'clean-healer-340010-6cfdd61db08b.json'
file_name = 'Twitter_Users'
sheet_name1 = 'シート1'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
# スプレッドシートにアクセス
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file, scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)
SPREADSHEET_KEY = '11DCjNA_20zeGn3rSxIYCYFbAzllq2KxS_FutiLjWZWA'

wb = gc.open_by_key(SPREADSHEET_KEY)
ws = wb.sheet1

def append_users(users):
    ws.append_row(users)

def judge_user_existence(user):
    return ws.find(user)