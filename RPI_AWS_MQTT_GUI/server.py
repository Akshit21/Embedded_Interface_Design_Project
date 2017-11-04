####################################################
# SAVE ON DRIVE.PY FILE
####################################################

import json
import sys
import socket
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

#Collecting data from sensors
def getData(worksheet):
    from collections import defaultdict
    weatherData=defaultdict(dict)
    
    while True:
        try:
            #Max Values
            weatherData['Max']['Temp']=worksheet.cell(4, 6).value
            weatherData['Max']['Hum']=worksheet.cell(4, 7).value
            weatherData['Max']['Time']=worksheet.cell(4, 8).value
            #Min Values
            weatherData['Min']['Temp']=worksheet.cell(6, 6).value
            weatherData['Min']['Hum']=worksheet.cell(6, 7).value
            weatherData['Min']['Time']=worksheet.cell(6, 8).value
            #Last Values
            weatherData['Last']['Temp']=worksheet.cell(8, 6).value
            weatherData['Last']['Hum']=worksheet.cell(8, 7).value
            weatherData['Last']['Time']=worksheet.cell(8, 8).value
            #Avg Values
            weatherData['Avg']['Temp']=worksheet.cell(10, 6).value
            weatherData['Avg']['Hum']=worksheet.cell(10, 7).value
            weatherData['Avg']['Time']=worksheet.cell(10, 8).value
            #Check if C or F
            weatherData['Unit']=worksheet.cell(14,7).value
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

#Collecting Messages and returning to the client
def getMessage(self,message):
    messageReturn='\n'+message
    weatherData=getData(self)
    print("Message:"+message)
    #print("Data:"+str(getData))
    # Last Temperature value
    if message=='LastTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Last']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Last']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Last']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Last']['Time']
    # Max Temp value
    elif message=='MaxTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Max']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Max']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Max']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Max']['Time']
   # Min Temp value
    elif message=='MinTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Min']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Min']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Min']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Min']['Time']
   # Avg Temp value
    elif message=='AvgTemp':
        if weatherData['Unit']=='F':
            messageReturn += '\nTemp: '+str(round((9.0/5.0) *float(weatherData['Avg']['Temp']) + 32.0,2))+ \
                            ' F' + '\nTime: '+ weatherData['Avg']['Time']
        else:
            messageReturn += '\nTemp: '+weatherData['Avg']['Temp'] + ' C' + \
                            '\nTime: '+ weatherData['Avg']['Time']
    #Last Humidity value
    elif message=='LastHum':
        messageReturn += '\nHumidity: '+weatherData['Last']['Hum'] +' %' + \
                        '\nTime: '+ weatherData['Last']['Time']
    # Max Humidity value
    elif message=='MaxHum':
        messageReturn += '\nHumidity: '+weatherData['Max']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Max']['Time']
    #Min Humidity value
    elif message=='MinHum':
        messageReturn += '\nHumidity: '+weatherData['Min']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Min']['Time']
    #Avg Hum value
    elif message=='AvgHum':
        messageReturn +='\nHumidity: '+weatherData['Avg']['Hum'] + ' %' + \
                        '\nTime: '+ weatherData['Avg']['Time']
    # Cto F conversion
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
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

commonPath="/home/pi/EID/Embedded_Interface_Design_Project/RPI_AWS_MQTT_GUI/cert/"

awshost = "a246go1f9auz2g.iot.us-east-2.amazonaws.com"
awsport = 8883
clientId = "MyRaspberryPi"
thingName = "MyRaspberryPi"
caPath = commonPath+"rootCA.pem"
certPath = commonPath+"f224d37fff-certificate.pem.crt"
keyPath = commonPath+"f224d37fff-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

worksheet= login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

while True:
    sleep(0.5)
    if connflag == True:
        weatherData = str(getData(worksheet))
        mqttc.publish("temperature", weatherData, qos=0)
        print("msg sent: Data " + weatherData )
    else:
        print("waiting for connection...")