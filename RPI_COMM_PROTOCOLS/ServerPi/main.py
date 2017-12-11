import json
import sys
import time
import datetime
import matplotlib.pyplot as plt
import Adafruit_DHT
import threading
import gspread
import logging
import argparse
from oauth2client.service_account import ServiceAccountCredentials
import paho.mqtt.client as mqtt
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import asyncio

import aiocoap.resource as resource
import aiocoap
import pika

start_time = 0

from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# GPIO PIN connection to Raspberry Pi
DHT_PIN  = 4

# JSON file contaning login info (should be in same dir as this file)
GDOCS_OAUTH_JSON = 'googleSheetAuth.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'EID'

# How long to wait (in seconds) between measurements.
WAIT_SECONDS = 3

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

####### QT GUI FOR  MEASURING WEATHER ###############
class Ui_Weather(QtGui.QWidget):
    # Creating Instance
    def __init__(self):
        super(Ui_Weather,self).__init__()
        self.tempList=[]
        self.humidityList=[]
        self.timeList=[]
        self.worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        self.count=2
        self.flag=True
        self.setupUi(self)
    # Setting up UI
    def setupUi(self, Weather):
        Weather.setObjectName(_fromUtf8("Weather"))
        Weather.resize(600, 600)
        self.verticalLayout = QtGui.QVBoxLayout(Weather)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mainLabel = QtGui.QLabel(Weather)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sitka Text"))
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(50)
        self.mainLabel.setFont(font)
        self.mainLabel.setStyleSheet(_fromUtf8("font: 18pt \"Sitka Text\";"))
        self.mainLabel.setObjectName(_fromUtf8("mainLabel"))
        self.verticalLayout.addWidget(self.mainLabel, QtCore.Qt.AlignHCenter)
        self.humLabel = QtGui.QLabel(Weather)
        self.humLabel.setObjectName(_fromUtf8("humLabel"))
        self.verticalLayout.addWidget(self.humLabel)
        self.humidityDisplay = QtGui.QTextBrowser(Weather)
        self.humidityDisplay.setObjectName(_fromUtf8("humidityDisplay"))
        self.verticalLayout.addWidget(self.humidityDisplay)
        self.tempLabel = QtGui.QLabel(Weather)
        self.tempLabel.setObjectName(_fromUtf8("tempLabel"))
        self.verticalLayout.addWidget(self.tempLabel)
        self.tempDisplay = QtGui.QTextBrowser(Weather)
        self.tempDisplay.setObjectName(_fromUtf8("tempDisplay"))
        self.verticalLayout.addWidget(self.tempDisplay)
        self.f2cButton = QtGui.QPushButton(Weather)
        self.f2cButton.setObjectName(_fromUtf8("f2cButton"))
        self.verticalLayout.addWidget(self.f2cButton)
        self.c2fButton = QtGui.QPushButton(Weather)
        self.c2fButton.setObjectName(_fromUtf8("c2fButton"))
        self.verticalLayout.addWidget(self.c2fButton)
        self.graphButton = QtGui.QPushButton(Weather)
        self.graphButton.setObjectName(_fromUtf8("graphButton"))
        self.verticalLayout.addWidget(self.graphButton)
        self.errorLabel = QtGui.QLabel(Weather)
        self.errorLabel.setObjectName(_fromUtf8("errorLabel"))
        self.verticalLayout.addWidget(self.errorLabel)
        self.errorDisplay = QtGui.QTextBrowser(Weather)
        self.errorDisplay.setObjectName(_fromUtf8("errorDisplay"))
        self.verticalLayout.addWidget(self.errorDisplay)

        self.retranslateUi(Weather)
        QtCore.QMetaObject.connectSlotsByName(Weather)
    
    def retranslateUi(self, Weather):
        Weather.setWindowTitle(_translate("Weather", "Weather", None))
        self.mainLabel.setText(_translate("Weather", "Weather Monitoring System", None))
        self.humLabel.setText(_translate("Weather", "Humidity", None))
        self.tempLabel.setText(_translate("Weather", "Temperature", None))
        self.f2cButton.setText(_translate("Weather", "F to C", None))
        self.c2fButton.setText(_translate("Weather", "C to F", None))
        self.graphButton.setText(_translate("Weather", "Plot Graph", None))
        self.errorLabel.setText(_translate("Weather", "Error", None))
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.saveData)
        self.my_timer.start(WAIT_SECONDS*1000)
        self.c2fButton.clicked.connect(self.updateFlagFalse)
        self.f2cButton.clicked.connect(self.updateFlagTrue)
        self.graphButton.clicked.connect(self.plotGraph)
    # When False update Farenheit
    def updateFlagFalse(self):
        self.worksheet.update_cell(14,7,'F')
        self.flag=False
    #When True update Celsius
    def updateFlagTrue(self):
        self.worksheet.update_cell(14,7,'C')
        self.flag=True
    # Graph plotting
    def plotGraph(self):
        plt.subplot(2,1,1)
        plt.plot(self.timeList,self.tempList)
        plt.xlabel('Time (sec)')
        plt.ylabel('Temp (C)')
        plt.title('Temperature Variance')
        plt.subplot(2,1,2)
        plt.plot(self.timeList,self.humidityList)
        plt.xlabel('Time (sec)')
        plt.ylabel('Humidity (%)')
        plt.title('Humidity Variance')
        plt.tight_layout()
        plt.show()
        #plt.savefig('graph.png',bbox_inches='tight')
    # Collecting Data
    def getData(self):
        while True:
            # Attempt to get sensor reading
            humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
            # Check if recieved valid measurements.
            # If not Try again till you get valid measurements
            if humidity is None or temp is None:
                self.errorDisplay.setText(_translate("Weather", "Error:Couldn't grab data properly @ "\
                                                     +str(datetime.datetime.now())+"\nTrying Again!!", None))
                self.tempDisplay.setText(_translate("Weather", " ", None))
                self.humidityDisplay.setText(_translate("Weather", " ", None))
                print ("Error:Couldn't grab data properly\nTrying Again!!")
                continue
            break
        self.temp=round(float(temp),2)
        self.humidity=round(float(humidity),2)
        self.tempList.append(temp)
        self.humidityList.append(humidity)
        self.timeVal=datetime.datetime.now()
        self.timeNow=time.time()
        self.timeList.append(self.timeNow)
    #Saving Data in worksheet
    def saveData(self):
        if self.worksheet is None:
            self.worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        while True:
            self.getData()
            self.maxTemp=round(max(self.tempList),2)
            self.minTemp=round(min(self.tempList),2)
            self.avgTemp=round((sum(self.tempList)/len(self.tempList)),2)
            self.maxHum=round(max(self.humidityList),2)
            self.minHum=round(min(self.humidityList),2)
            self.avgHum=round((sum(self.humidityList)/len(self.humidityList)),2)
            try:
                #Keep on storing the values
                self.worksheet.update_cell(self.count, 1, self.timeVal)
                self.worksheet.update_cell(self.count, 2, self.temp)
                self.worksheet.update_cell(self.count, 3, self.humidity)
                #Max Values
                self.worksheet.update_cell(4,6,self.maxTemp)
                self.worksheet.update_cell(4,7,self.maxHum)
                self.worksheet.update_cell(4,8,self.timeVal)
                #Min Values
                self.worksheet.update_cell(6,6,self.minTemp)
                self.worksheet.update_cell(6,7,self.minHum)
                self.worksheet.update_cell(6,8,self.timeVal)
                #Last Values
                self.worksheet.update_cell(8,6,self.temp)
                self.worksheet.update_cell(8,7,self.humidity)
                self.worksheet.update_cell(8,8,self.timeVal)
                #Avg Values
                self.worksheet.update_cell(10,6,self.avgTemp)
                self.worksheet.update_cell(10,7,self.avgHum)
                self.worksheet.update_cell(10,8,self.timeVal)
                #Increment the cell
                self.count+=1
                print("Updated Data on Google Sheet")
                #Update on GUI
                if self.flag :
                    self.tempDisplay.setText(_translate("Weather", \
                                                        "Last: "+str(self.temp)+ " C\nTime:" + str(self.timeVal) + \
                                                        "\n\nMax: "+str(self.maxTemp)+ " C\nTime:" + str(self.timeVal) + \
                                                        "\n\nMin: "+str(self.minTemp)+ " C\nTime: " + str(self.timeVal) + \
                                                        "\n\nAvg: "+str(self.avgTemp)+ " C\nTime: " + str(self.timeVal) \
                                                        , None))
                else :
                    self.tempDisplay.setText(_translate("Weather", \
                                                        "Last: "+str(round((9.0/5.0) * self.temp + 32.0,2))+ " F\nTime:" + str(self.timeVal) + \
                                                        "\n\nMax: "+str(round((9.0/5.0) * self.maxTemp + 32.0,2))+ " F\nTime:" + str(self.timeVal) + \
                                                        "\n\nMin: "+str(round((9.0/5.0) * self.minTemp + 32.0,2))+ " F\nTime:" + str(self.timeVal) + \
                                                        "\n\nAvg: "+str(round((9.0/5.0) * self.avgTemp + 32.0,2))+ " F\nTime:" + str(self.timeVal) \
                                                        , None))
                    #displaying  humidity
                self.humidityDisplay.setText(_translate("Weather", \
                                                    'Last: '+str(self.humidity)+ ' %\nTime:' + str(self.timeVal) + \
                                                    '\n\nMax: '+str(self.maxHum)+ ' %\nTime:' + str(self.timeVal) + \
                                                    '\n\nMin: '+str(self.minHum)+ ' %\nTime:' + str(self.timeVal) + \
                                                    '\n\nAvg: '+str(self.avgHum)+ ' %\nTime:' + str(self.timeVal) \
                                                    , None))

            except Exception as e:
                # Error appending data, most likely because credentials are stale.
                # Null out the self.worksheet so a login is performed at the top of the loop.
                print("Error:" + str(e))
                print('Trying to Login again. Check connections!!')
                self.errorDisplay.setText(_translate("Weather", str(e), None))
                self.tempDisplay.setText(_translate("Weather", " ", None))
                self.humidityDisplay.setText(_translate("Weather", " ", None))
                self.worksheet = None
                time.sleep(WAIT_SECONDS)
                continue
            break
    

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    
def on_message(mqttc, obj, msg):
    mqttc.publish("/EID",str(msg.payload))
    
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def mqtt_connection_thread():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.connect("10.0.0.17", 1883, 60)
    mqttc.subscribe("/EID", 0)
    mqttc.loop_forever()

# Creating class handlers
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
   #  Receiving messages from client
    def on_message(self, message):
        print ('message received:  %s' % message)
        self.write_message(message)

    #Closing the client connection
    def on_close(self):
        print ('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/ws', WSHandler)
])

def ws_connection_thread():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
    
class BlockResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=request.payload)


class SeparateLargeResource(resource.Resource):
    """Example resource which supports the GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first. """

    def get_link_description(self):
        # Publish additional data in .well-known/core
        return dict(**super().get_link_description(), title="A large resource")

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = "Three rings for the elven kings under the sky, seven rings "\
                "for dwarven lords in their halls of stone, nine rings for "\
                "mortal men doomed to die, one ring for the dark lord on his "\
                "dark throne.".encode('ascii')
        return aiocoap.Message(payload=payload)

class TimeResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.handle = self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().\
                strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

class coap_main():
    def coap_conn(self):
        # Resource tree creation
        root = resource.Site()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        root.add_resource(('.well-known', 'core'),
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(('time',), TimeResource())
        root.add_resource(('other', 'block'), BlockResource())
        root.add_resource(('other', 'separate'), SeparateLargeResource())

        asyncio.Task(aiocoap.Context.create_server_context(root))
        asyncio.get_event_loop().run_forever()
        
class amqp_init:
    def __init__(self):
        self.channel = None
        self.exchange = None
        self.connection = None
        self.queue = None
        self.consume_tag=None
        
    def amqp_on_connection_open(self, unused_connection):
        print("connection opened")
        self.channel=self.connection.channel(on_open_callback=self.amqp_on_channel_open)
        
    def amqp_on_channel_open(self,ch):
        print("channel opened")
        self.exchange = self.channel.exchange_declare(self.amqp_on_exchange_declareok,"eid_exchange",'topic')
        
    def amqp_on_exchange_declareok(self,unused_frame):
        print("exchange declared")
        self.queue= self.channel.queue_declare(self.amqp_on_queue_declareok, 'eid_queue')
        
    def amqp_on_queue_declareok(self,method_frame):
        print("queue declared")
        self.channel.queue_bind(self.amqp_on_bindok, 'eid_queue','eid_exchange', 'example.text')
        
    def amqp_on_bindok(self,unused_frame):
        print("binded with the queue")
        self.consume_tag = self.channel.basic_consume(self.amqp_on_message,'eid_queue')
        
    def establish_conn(self):
        self.connection = pika.SelectConnection(pika.URLParameters('amqp://eid:eid@10.0.0.17:5672'),on_open_callback=self.amqp_on_connection_open,)
        self.connection.ioloop.start()
        
    def publish_string(self,string):
        properties = pika.BasicProperties(app_id='server',content_type='application/json')
        self.channel.basic_publish('eid_exchange','example.text',string,properties)
        
    def amqp_on_message(self, unused_channel, basic_deliver, properties, body):
        if(properties.app_id == 'client'):
            self.channel.basic_ack(basic_deliver.delivery_tag)
            print(properties.app_id)
            self.publish_string(body)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    weatherGui = QtGui.QWidget()
    ui = Ui_Weather()
    ui.setupUi(weatherGui)
    mqtt_thread = threading.Thread(target = mqtt_connection_thread, name='mqtt_thread')
    mqtt_thread.start()
    ws_thread = threading.Thread(target = ws_connection_thread, name='ws_thread')
    ws_thread.start()
    coap_main = coap_main()
    coap_thread = threading.Thread(target= coap_main.coap_conn, name='coap_thread')
    coap_thread.start()
    amqp = amqp_init()
    amqp_thread = threading.Thread(target = amqp.establish_conn,name='amqp_thread')
    amqp_thread.start()
    weatherGui.show()
    sys.exit(app.exec_())
