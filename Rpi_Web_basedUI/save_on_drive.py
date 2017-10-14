#!/usr/bin/python
#
# Google Spreadsheet DHT Sensor Data-logging
# Citation : https://github.com/adafruit/Adafruit_Python_DHT
#
#

import json
import sys
import time
import datetime

import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# GPIO PIN connection to Raspberry Pi
DHT_PIN  = 4

# JSON file contaning login info (should be in same dir as this file)
GDOCS_OAUTH_JSON       = 'eidproject.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'EID'

# How long to wait (in seconds) between measurements.
WAIT_SECONDS      = 5

# Method to get login credentials and open the spread sheet
def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        scope =  ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name,' +
                'and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)
        
def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, WAIT_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
count=2
tempList=[]
humidityList=[]
while True:
    # Login if necessary.
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
    # Check if recieved valid measurements.
    # If not Try again till you get valid measurements
    if humidity is None or temp is None:
        print ("Error:Couldn't grab data properly\nTrying Again!!")
        time.sleep(2)
        continue
    temp=round(float(temp),2)
    humidity=round(float(humidity),2)
    #timeVal = datetime.datetime.now() # Should I display this?
    tempList.append(temp)
    humidityList.append(humidity)
##    key = getchar()
##    if key == 'f'or key == 'F':
##        tempF = (temp * 1.8) + 32
##        print('Temperature: {0:0.1f} F'.format(tempF))
##    else:
##        print('Temperature: {0:0.1f} C'.format(temp))
    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    # Append the data in the spreadsheet, including a timestamp
    try:
        #All Values
        worksheet.update_cell(count, 1, datetime.datetime.now())
        worksheet.update_cell(count, 2, temp)
        worksheet.update_cell(count, 3, humidity)
	#Max Values
        worksheet.update_cell(4,6,max(tempList))
        worksheet.update_cell(4,7,max(humidityList))
        worksheet.update_cell(4,8,datetime.datetime.now())
        #Min Values
        worksheet.update_cell(6,6,min(tempList))
        worksheet.update_cell(6,7,min(humidityList))
        worksheet.update_cell(6,8,datetime.datetime.now())
	#Last Values
        worksheet.update_cell(8,6,temp)
        worksheet.update_cell(8,7,humidity)
        worksheet.update_cell(8,8,datetime.datetime.now())
        #Avg Values
        worksheet.update_cell(10,6,round((sum(tempList)/len(tempList)),2))
        worksheet.update_cell(10,7,round((sum(humidityList)/len(humidityList)),2))
        worksheet.update_cell(10,8,datetime.datetime.now())
        count+=1
    except Exception as e:
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print("Error:" + str(e))
        print('Trying to Login again. Check connections!!')
        worksheet = None
        time.sleep(WAIT_SECONDS)
        continue

    # Wait 30 seconds before continuing
    print('Wrote a row to {0} Spread Sheet'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(WAIT_SECONDS)
