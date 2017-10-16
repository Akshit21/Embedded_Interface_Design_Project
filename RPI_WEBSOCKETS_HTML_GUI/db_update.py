import json
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# JSON file contaning login info (should be in same dir as this file)
GDOCS_OAUTH_JSON       = 'eidproject.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'EID'

# How long to wait (in seconds) between measurements.
WAIT_SECONDS      = 5

# Method to get login credentials and open the spread sheet
class db():
       def login_open_sheet(self,oauth_key_file, spreadsheet):
           try:
               scope =  ['https://spreadsheets.google.com/feeds']
               credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
               gc = gspread.authorize(credentials)
               worksheet = gc.open(spreadsheet).sheet1
               print(' Credentials fetched')
               weatherData = defaultdict(dict)
               print('hello')
               while True:
                 try:
                        print('Entering the loop')
                        #Max Values
                        weatherData['Max']['Temp'] = worksheet.cell(4, 6).value
                        weatherData['Max']['Hum'] = worksheet.cell(4, 7).value
                        weatherData['Max']['Time'] = worksheet.cell(4, 8).value
                        #Min Values
                        weatherData['Min']['Temp'] = worksheet.cell(6, 6).value
                        weatherData['Min']['Hum'] = worksheet.cell(6, 7).value
                        weatherData['Min']['Time'] = worksheet.cell(6, 8).value
                        #Last Values
                        weatherData['Last']['Temp'] = worksheet.cell(8, 6).value
                        weatherData['Last']['Hum'] = worksheet.cell(8, 7).value
                        weatherData['Last']['Time'] = worksheet.cell(8, 8).value
                        #Avg Values
                        weatherData['Avg']['Temp'] = worksheet.cell(10, 6).value
                        weatherData['Avg']['Hum'] = worksheet.cell(10, 7).value
                        weatherData['Avg']['Time'] = worksheet.cell(10, 8).value
                        print('\n Last Temp:' +weatherData['Last']['Temp'] )
                        break
                 except Exception as e:
                      # Error appending data, most likely because credentials are stale.
                      # Null out the worksheet so a login is performed at the top of the loop.
                        print("Error:" + str(e))
                        print('Trying to Login again. Check connections!!')
                        while worksheet is None:
                              worksheet= login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
                        continue
               return weatherData

           except Exception as ex:
               print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name,' +
                     'and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
               print('Google sheet login failed with error:', ex)
               sys.exit(1)

def main():

     q = db()
     q.login_open_sheet('eidproject.json', 'EID')

if __name__ == '__main__':
     main()
