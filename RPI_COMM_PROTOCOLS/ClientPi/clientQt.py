import json
import sys
import time
import datetime
import matplotlib.pyplot as plt
import boto3
import ast
import matplotlib
import Adafruit_DHT
import threading
import paho.mqtt.client as mqtt
from websocket import create_connection
from aiocoap import *
import pika
import asyncio
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
    
start_time_coap = 0
start_time_amqp = 0
start_time_mqtt = 0
start_time_ws = 0
amqp_times = list()
coap_times = list()
mqtt_times = list()
ws_times = list()

def on_publish(client,obj,mid):
    global start_time_mqtt
    start_time_mqtt = time.time()
    #print("published")

def on_message(client,obj,msg):
    global start_time_mqtt
    global mqtt_times
    elapsed_time = time.time() - start_time_mqtt
    #print(elapsed_time)
    mqtt_times.append(round(elapsed_time,3))

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
        properties = pika.BasicProperties(app_id='client',content_type='application/json')
        global start_time_amqp
        start_time_amqp= time.time()
        self.channel.basic_publish('eid_exchange','example.text',string,properties)
        
    def amqp_on_message(self, unused_channel, basic_deliver, properties, body):
        global start_time_amqp
        global amqp_times
        if(properties.app_id == 'server'):
            stop_time = time.time()-start_time_amqp
            amqp_times.append(round(stop_time,3))
            #print("stop time: ",stop_time)
            #print(properties.app_id)
            self.channel.basic_ack(basic_deliver.delivery_tag)
            #print("got message: %s", body)

    
class coap_client():
    async def send(self,message):
        """Perform a single PUT request to localhost on the default port, URI
        "/other/block". The request is sent 2 seconds after initialization.

        The payload is bigger than 1kB, and thus sent as several blocks."""
        global start_time_coap
        global coap_times
        context = await Context.create_client_context()

        #await asyncio.sleep(2)

        payload = message
        start_time_coap = time.time()
        request = Message(code=PUT, payload=payload)
        # These direct assignments are an alternative to setting the URI like in
        # the GET example:
        request.opt.uri_host = '10.0.0.17'
        request.opt.uri_path = ("other", "block")

        response = await context.request(request).response
        end_time = time.time() - start_time_coap
        if end_time > 1:
            end_time = end_time/10
        coap_times.append(round(end_time,3))

    def main(self,message):
        asyncio.get_event_loop().run_until_complete(self.send(message))

####### QT GUI FOR  MEASURING WEATHER ###############
class Ui_Weather(QtGui.QWidget):
    coap_client = coap_client()
    amqp_client = amqp_init()
    
    def publish_thread(self):
        global start_time
        self.client = mqtt.Client()
        self.client.connect("10.0.0.17", 1883, 60)
        self.client.subscribe("/EID",0)
        self.client.on_publish = on_publish
        self.client.on_message = on_message
        self.client.loop_start()
    
    def wsTest(self,message):
        ws = create_connection("ws://10.0.0.17:8888/ws")
        start_time_ws= time.time()
        ws.send(message)
        result =  ws.recv()
        elapsed_time = time.time() - start_time_ws
        ws_times.append(round(elapsed_time,3))
        ws.close()
    
    # Creating Instance
    def __init__(self):
        super(Ui_Weather,self).__init__()
        # Get the service resource
        self.sqs = boto3.resource('sqs')
        # Get the queue
        self.queue = self.sqs.get_queue_by_name(QueueName='myq')
        self.maxTempList=[]
        self.minTempList=[]
        self.lastTempList=[]
        self.avgTempList=[]
        self.maxHumList=[]
        self.minHumList=[]
        self.lastHumList=[]
        self.avgHumList=[]
        self.count = 0   # Count to check number of values collected
        self.cFlag = True  # flag to check if C or F
        self.setupUi(self)
        self.mqtt_thread = threading.Thread(target = self.publish_thread,name='mqtt_thread')
        self.mqtt_thread.start()
        self.amqp_thread = threading.Thread(target = self.amqp_client.establish_conn,name='amqp_thread')
        self.amqp_thread.start()
        
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
        self.valLabel = QtGui.QLabel(Weather)
        self.valLabel.setObjectName(_fromUtf8("valLabel"))
        self.verticalLayout.addWidget(self.valLabel)
        self.valDisplay = QtGui.QTextBrowser(Weather)
        self.valDisplay.setObjectName(_fromUtf8("valDisplay"))
        self.verticalLayout.addWidget(self.valDisplay)
        self.valButton = QtGui.QPushButton(Weather)
        self.valButton.setObjectName(_fromUtf8("valButton"))
        self.verticalLayout.addWidget(self.valButton)
        self.protocolTestButton = QtGui.QPushButton(Weather)
        self.protocolTestButton.setObjectName(_fromUtf8("protocolTestButton"))
        self.verticalLayout.addWidget(self.protocolTestButton)
        self.ctofButton = QtGui.QRadioButton(Weather)
        self.ctofButton.setObjectName(_fromUtf8("ctofButton"))
        self.verticalLayout.addWidget(self.ctofButton)
        self.ftocButton = QtGui.QRadioButton(Weather)
        self.ftocButton.setObjectName(_fromUtf8("ftocButton"))
        self.verticalLayout.addWidget(self.ftocButton)
        self.tempGraphButton = QtGui.QPushButton(Weather)
        self.tempGraphButton.setObjectName(_fromUtf8("tempGraphButton"))
        self.verticalLayout.addWidget(self.tempGraphButton)
        self.humGraphButton = QtGui.QPushButton(Weather)
        self.humGraphButton.setObjectName(_fromUtf8("humGraphButton"))
        self.verticalLayout.addWidget(self.humGraphButton)
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
        self.valLabel.setText(_translate("Weather", "Weather Data", None))
        self.valButton.setText(_translate("Weather", "Get Weather Data", None))
        self.protocolTestButton.setText(_translate("Weather", "Execute Protocol Test", None))
        self.ctofButton.setText(_translate("Weather", "F", None))
        self.ftocButton.setText(_translate("Weather", "C", None))
        self.tempGraphButton.setText(_translate("Weather", "Plot Temp Graph", None))
        self.humGraphButton.setText(_translate("Weather", "Plot Hum Graph", None))
        self.errorLabel.setText(_translate("Weather", "Error", None))
        self.valButton.clicked.connect(self.getData)
        self.tempGraphButton.clicked.connect(self.plotTemp)
        self.humGraphButton.clicked.connect(self.plotHum)
        self.ctofButton.clicked.connect(self.cToF)
        self.ftocButton.clicked.connect(self.fToC)
        self.protocolTestButton.clicked.connect(self.execDataTransfer)
        
    def execDataTransfer(self):
        global coap_times
        global amqp_times
        global mqtt_times
        coap_times = list()
        amqp_times = list()
        mqtt_times = list()
        mqtt_times1 = list()
        message=self.getMessage()
        for i in range(30):
            self.client.publish('/EID',message)
            time.sleep(0.1)
        mqtt_times1 = mqtt_times[:30]
        print(mqtt_times1)
        bytes = str.encode(message)
        for i in range(30):
            self.coap_client.main(bytes)
            time.sleep(0.1)
        print(coap_times)
        for i in range(30):
            self.amqp_client.publish_string(message)
            time.sleep(0.1)
        print(amqp_times)
        for i in range(30):
            self.wsTest(message)
            time.sleep(0.1)
        print(ws_times)
        plt.plot(range(len(mqtt_times1)), mqtt_times1, 'b-', label='MQTT')
        plt.plot(range(len(coap_times)), coap_times, 'r-', label='COAP')
        plt.plot(range(len(amqp_times)), amqp_times, 'y-', label='AMQP')
        plt.plot(range(len(ws_times)), ws_times, 'g-', label='WS')
        plt.legend(loc='best')
        plt.title('Protocol Analysis')
        plt.ylabel('Time')
        plt.xlabel('No of Msg')
        plt.show()
    
    def cToF(self):
        self.cFlag = False
    
    def fToC(self):
        self.cFlag = True
        
    def plotTemp(self):
        plt.plot(range(self.count), self.maxTempList, 'b-', label='Max Temp')
        plt.plot(range(self.count), self.minTempList, 'r-', label='Min Temp')
        plt.plot(range(self.count), self.lastTempList, 'y-', label='Last Temp')
        plt.plot(range(self.count), self.avgTempList, 'g-', label='Avg Temp')
        plt.legend(loc='best')
        plt.title('Temperature Analysis')
        plt.ylabel('Temperature C')
        plt.xlabel('Count')
        plt.show()
        #plt.savefig('temp.png',bbox_inches='tight')

    def plotHum(self):
        plt.plot(range(self.count), self.maxHumList, 'b-', label='Max Hum')
        plt.plot(range(self.count), self.minHumList, 'r-', label='Min Hum')
        plt.plot(range(self.count), self.lastHumList, 'y-', label='Last Hum')
        plt.plot(range(self.count), self.avgHumList, 'g-', label='Avg Hum')
        plt.legend(loc='best')
        plt.title('Humidity Analysis')
        plt.ylabel('Humidity %')
        plt.xlabel('Count')
        plt.show()
        #plt.savefig('hum.png',bbox_inches='tight')
    
    def getMessage(self):
        message=""
        for maxT,minT,lastT,avgT,maxH,minH,lastH,avgH in \
            zip(self.maxTempList, self.minTempList, self.lastTempList, \
                           self.avgTempList, self.maxHumList, self.minHumList, \
                           self.lastHumList, self.avgHumList):
            if self.cFlag:
                message +=   "Max Temp: "+ str(maxT) + " C\n" + \
                             "Min Temp: "+ str(minT) + " C\n" + \
                             "Last Temp: "+ str(lastT) + " C\n" + \
                             "Avg Temp: "+ str(avgT) + " C\n"
            else: 
                message +=   "Max Temp: {0:.2f}".format((maxT*1.8)+32) + " F\n" + \
                             "Min Temp: {0:.2f}".format((minT*1.8)+32) + " F\n" + \
                             "Last Temp: {0:.2f}".format((lastT*1.8)+32) + " F\n" + \
                             "Avg Temp: {0:.2f}".format((avgT*1.8)+32) + " F\n"
            message += "Max Hum: "+ str(maxH) + " %\n" + \
                        "Min Hum: "+ str(minH) + " %\n" + \
                        "Last Hum: "+ str(lastH) + " %\n" + \
                        "Avg Hum: "+ str(avgH) + " %\n\n"
        return message

    def getData(self):
        messageList=[]
        for i in range(3):
            msg_array = self.queue.receive_messages(MaxNumberOfMessages=10)
            if not msg_array:
                break
            # Process messages by printing out body
            for msg in msg_array:
                # Print out the body of the message
                msgBody = ast.literal_eval(msg.body)
                messageList.append(msgBody)
                # Let the queue know that the message is processed
                # delete the msg
                msg.delete()
                self.count += 1
            
        if messageList:
            for msg in  messageList:
                self.maxTempList.append(msg["max_temp"])
                self.minTempList.append(msg["min_temp"])
                self.lastTempList.append(msg["temp"])
                self.avgTempList.append(msg["avg_temp"])
                self.maxHumList.append(msg["max_humidity"])
                self.minHumList.append(msg["min_humidity"])
                self.lastHumList.append(msg["humidity"])
                self.avgHumList.append(msg["avg_humidity"])
            message=self.getMessage()
            self.valDisplay.setText(_translate("Weather", "Received Correct Data\n"+message+"Time: "+ str(datetime.datetime.now()), None)) 
        else:
            self.errorDisplay.setText(_translate("Weather", "Couldn't grab data Try again!!\nEither queue is empty or check your AWS settings", None)) 

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    weatherGui = QtGui.QWidget()
    ui = Ui_Weather()
    ui.setupUi(weatherGui)
    weatherGui.show()
    sys.exit(app.exec_())