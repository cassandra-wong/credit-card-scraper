import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

def upload_gsheet(csv_file):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('gsheet_client.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('Canadian CC Bonus Scraper')

    with open(csv_file, 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)
    
    worksheet = spreadsheet.get_worksheet(0)
    worksheet.update_title(f"Last Updated: {today}")

if __name__ == "__main__":
    upload_gsheet('formatted_file.csv')