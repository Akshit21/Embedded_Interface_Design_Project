####################################################
# SAVE ON DRIVE.PY FILE
####################################################

import json
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# JSON file contaning login info (should be in same dir as this file)
GDOCS_OAUTH_JSON       = 'googleSheetAuth.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'EID'

# How long to wait (in seconds) between measurements.
WAIT_SECONDS      = 5

# Method to get login credentials and open the spread sheet
def login_open_sheet(oauth_key_file, spreadsheet):
    while(1):
        try:
            scope =  ['https://spreadsheets.google.com/feeds']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
            gc = gspread.authorize(credentials)
            worksheet = gc.open(spreadsheet).sheet1
            break
        except Exception as ex:
            print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name,' +
                    'and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
            print('Google sheet login failed with error:', ex)
            print("Trying again")
            time.sleep(WAIT_SECONDS)
    return worksheet

def getData(self):
    from collections import defaultdict
    weatherData=defaultdict(dict)
    while True:
        try:
            #Max Values
            weatherData['Max']['Temp']=self.worksheet.cell(4, 6).value
            weatherData['Max']['Hum']=self.worksheet.cell(4, 7).value
            weatherData['Max']['Time']=self.worksheet.cell(4, 8).value
            #Min Values
            weatherData['Min']['Temp']=self.worksheet.cell(6, 6).value
            weatherData['Min']['Hum']=self.worksheet.cell(6, 7).value
            weatherData['Min']['Time']=self.worksheet.cell(6, 8).value
            #Last Values
            weatherData['Last']['Temp']=self.worksheet.cell(8, 6).value
            weatherData['Last']['Hum']=self.worksheet.cell(8, 7).value
            weatherData['Last']['Time']=self.worksheet.cell(8, 8).value
            #Avg Values
            weatherData['Avg']['Temp']=self.worksheet.cell(10, 6).value
            weatherData['Avg']['Hum']=self.worksheet.cell(10, 7).value
            weatherData['Avg']['Time']=self.worksheet.cell(10, 8).value
            #Check if C or F
            weatherData['Unit']=self.worksheet.cell(14,7).value
            break
        except Exception as e:
            # Error appending data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print("Error:" + str(e))
            print('Trying to Login again. Check connections!!')
            while self.worksheet is None:
                self.worksheet= login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
            continue
    return weatherData

def getMessage(self,message):
    messageReturn='\n'+message
    weatherData=getData(self)
    print("Message:"+message)
    #print("Data:"+str(getData))
    if message=='LastTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Last']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Last']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Last']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Last']['Time']
    elif message=='MaxTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Max']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Max']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Max']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Max']['Time']
    elif message=='MinTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Min']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Min']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Min']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Min']['Time']
    elif message=='AvgTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Avg']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Avg']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Avg']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Avg']['Time']
    elif message=='LastHum':
        messageReturn += '\nHumidity: '+weatherData['Last']['Hum'] +' %' + \
                        '\nTime: '+ weatherData['Last']['Time']
    elif message=='MaxHum':
        messageReturn += '\nHumidity: '+weatherData['Max']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Max']['Time']
    elif message=='MinHum':
        messageReturn += '\nHumidity: '+weatherData['Min']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Min']['Time']
    elif message=='AvgHum':
        messageReturn +='\nHumidity: '+weatherData['Avg']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Avg']['Time']
    elif message=='CtoF':
        farenheit1 = ((9.0/5.0) * (float(weatherData['Last']['Temp']))) + 32.0
        farenheit2 = ((9.0/5.0) * (float(weatherData['Max']['Temp']))) + 32.0
        farenheit3 = ((9.0/5.0) * (float(weatherData['Min']['Temp']))) + 32.0
        farenheit4 = ((9.0/5.0) * (float(weatherData['Avg']['Temp']))) + 32.0
        messageReturn +='\n Last Temp:' +str(farenheit1) + 'F' + \
                        '\n Max Temp:' +str(farenheit2) + 'F' + \
                        '\n Min Temp:'  +str(farenheit3) + 'F' +\
                        '\n Avg Temp:' +str(farenheit4) + 'F'

    else:
        messageReturn ='Invalid Message'
    return messageReturn

####################################################
# SERVER.PY FILE
####################################################
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes.
'''
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        print ('new connection')
    def on_message(self, message):
        print ('message received:  %s' % message)
        if "login" in message:
            validate=message.split(" ")
            if validate[1]== 'Weather' and validate[2]=='Rpi3':
                self.write_message('OK')
            else:
                self.write_message('NOT')
        else:
            weatherData = getMessage(self,message)
            print("WeatherData:"+weatherData)
            self.write_message(weatherData)

    def on_close(self):
        print ('connection closed')

    def check_origin(self, origin):
        return True

    	
application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r"/(graph.png)", tornado.web.StaticFileHandler, {'path':'./'})
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
