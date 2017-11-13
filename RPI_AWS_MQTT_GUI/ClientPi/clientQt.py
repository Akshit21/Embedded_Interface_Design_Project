import json
import sys
import time
import datetime
import matplotlib.pyplot as plt
import boto3
import ast
import matplotlib
import Adafruit_DHT

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

####### QT GUI FOR  MEASURING WEATHER ###############
class Ui_Weather(QtGui.QWidget):
    # Creating Instance
    def __init__(self):
        super(Ui_Weather,self).__init__()
        # Get the service resource
        self.sqs = boto3.resource('sqs')
        # Get the queue
        self.queue = self.sqs.get_queue_by_name(QueueName='statq')
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
    #providing functionality for the buttons
    def retranslateUi(self, Weather):
        Weather.setWindowTitle(_translate("Weather", "Weather", None))
        self.mainLabel.setText(_translate("Weather", "Weather Monitoring System", None))
        self.valLabel.setText(_translate("Weather", "Weather Data", None))
        self.valButton.setText(_translate("Weather", "Get Weather Data", None))
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
    
    def cToF(self):
        self.cFlag = False
    
    def fToC(self):
        self.cFlag = True
        #plotting temperature values
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
#Plotting humidity values
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
    #parsing the received message from sqs and storing them in right format
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
#Pulling a fixed number of messages for plotting it on qt
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
     #displaying messages in qt       
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
            self.valDisplay.setText(_translate("Weather", "Received Correct Data\n"+message, None)) 
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
