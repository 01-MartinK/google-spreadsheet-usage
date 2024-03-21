import argparse

parser = argparse.ArgumentParser(description='gives newsletter')

parser.add_argument('email', metavar='email', type=str, help="enter email")
parser.add_argument('sheetId', metavar='sheetId', type=str, help="enter sheetId")

args = parser.parse_args()

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds = Credentials.from_service_account_file("credentialsService.json")
  # If there are no (valid) credentials available, let the user log in.

  try:
    service = build("sheets", "v4", credentials=creds)
    write_value(service)
  except HttpError as err:
    print(err)

def write_value(service):
  spreadsheet_id = args.sheetId
  
  sheets = service.spreadsheets()

  sheets.values().append(spreadsheetId=spreadsheet_id, range="A2", valueInputOption="USER_ENTERED", body={"values": [[args.email]]}).execute()

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