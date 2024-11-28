import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe


scopes = ["https://oauth2.googleapis.com/token"]
creds = Credentials.from_service_account_file("key.json", scopes= scopes)
client = gspread.authorize(creds)
sheet_to = "1SQ7XsnvF39EY1b-z-OYtJirSu2-bjrZ7ORmMfLVQK5Q"
workbook2 = client.open_by_key(sheet_to)
topshiriq = workbook2.worksheet("ochiq xat")

def get_from_google():
    data = get_as_dataframe(topshiriq, drop_empty_columns=True, drop_empty_rows=True)
    df = data[['nomer', 'javobgar', 'Status','Natijasi']]
    
    return df

res = get_from_google()
