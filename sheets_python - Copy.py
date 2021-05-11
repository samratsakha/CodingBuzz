import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('codingbuzz_credentials.json',scope)

client = gspread.authorize(credentials)
sheet = client.open("codingbuzz_login_database").sheet1

data = sheet.get_all_records()
email = [item for item in sheet.col_values(1) if item]
password = [item for item in sheet.col_values(2) if item]

for i in range(0,len(email)):
    print(email[i],password[i])

len_row = len(email)

sheet.update_cell(len_row+1,1,"YES")


