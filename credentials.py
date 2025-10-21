import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "spreadsheet-id"
SAMPLE_RANGE_NAME = "Class Data!A2:E"

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    write_range(service)
  except HttpError as err:
    print(err)

def create(service):
    spreadsheet_details = {
    'properties': {
        'title': 'Python-google-sheets-demo'
        }
    }
    sheet = service.spreadsheets().create(body=spreadsheet_details,
                                    fields='spreadsheetId').execute()
    
    sheetId = sheet.get('spreadsheetId')
    service.spreadsheets().values().append(spreadsheetId=sheetId, range="A1", valueInputOption="USER_ENTERED", body={"values": [["name", "email", "phone"]]}).execute()
    print('Spreadsheet ID: {0}'.format(sheetId))
    return sheetId

def write_range(service):
  file_id = get_file()
  spreadsheet_id = ""
  
  if not file_id:
    spreadsheet_id = create(service)
    create_file(spreadsheet_id)
  else:
    spreadsheet_id = file_id
  
  sheets = service.spreadsheets()
  
  for row in range(2, 8):
    sheets.values().append(spreadsheetId=spreadsheet_id, range="A2", valueInputOption="USER_ENTERED", body={"values": [["test", "test2", "test3"]]}).execute()
    #sheets.values().append(spreadsheetId=spreadsheet_id, range=("B"+str(row)), valueInputOption="USER_ENTERED", body={"values": [["Done"]]}).execute()

# Get the file with the ID
def get_file():
  try:
    f = open("sheetId.txt", "r")
    return f.read()
  except FileNotFoundError as err:
    print(err)

# Create the file with the ID
def create_file(content):
  try:
    f = open("sheetId.txt", "w")
    f.write(content)
  except FileExistsError as err:
    print(err)

if __name__ == "__main__":
  main()
