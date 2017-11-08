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
        self.queue = self.sqs.get_queue_by_name(QueueName='Weather.fifo')
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
        self.tempGraphButton.setText(_translate("Weather", "Plot Temp Graph", None))
        self.humGraphButton.setText(_translate("Weather", "Plot Hum Graph", None))
        self.errorLabel.setText(_translate("Weather", "Error", None))
        self.valButton.clicked.connect(self.getData)
        self.tempGraphButton.clicked.connect(self.plotTemp)
        self.humGraphButton.clicked.connect(self.plotHum)
        
    def plotTemp(self):
        timeList1 = [datetime.datetime.strptime(val,'%Y-%m-%d %H:%M:%S') for val in self.timeStamp]
        timeList = matplotlib.dates.date2num(timeList1)
        plt.plot(timeList, self.maxTempList, 'b-', label='Max Temp')
        plt.plot(timeList, self.minTempList, 'r-', label='Min Temp')
        plt.plot(timeList, self.lastTempList, 'y-', label='Last Temp')
        plt.plot(timeList, self.avgTempList, 'g-', label='Avg Temp')
        plt.legend(loc='best')
        plt.title('Temperature Analysis')
        plt.ylabel('Temperature C')
        plt.xlabel('Time Stamp')
        plt.show()
        #plt.savefig('temp.png',bbox_inches='tight')

    def plotHum(self):
        timeList1 = [datetime.datetime.strptime(val,'%Y-%m-%d %H:%M:%S') for val in self.timeStamp]
        timeList = matplotlib.dates.date2num(timeList1)
        plt.plot(timeList, self.maxHumList, 'b-', label='Max Hum')
        plt.plot(timeList, self.minHumList, 'r-', label='Min Hum')
        plt.plot(timeList, self.lastHumList, 'y-', label='Last Hum')
        plt.plot(timeList, self.avgHumList, 'g-', label='Avg Hum')
        plt.legend(loc='best')
        plt.title('Humidity Analysis')
        plt.ylabel('Humidity %')
        plt.xlabel('Time Stamp')
        plt.show()
        #plt.savefig('hum.png',bbox_inches='tight')
    
    def getMessage(self):
        message=""
        for maxT,minT,lastT,avgT,maxH,minH,lastH,avgH,timeS in \
            zip(self.maxTempList, self.minTempList, self.lastTempList, \
                           self.avgTempList, self.maxHumList, self.minHumList, \
                           self.lastHumList, self.avgHumList, self.timeStamp):
            message+="Max Temp: "+ str(maxT) + " C\t Time: " + timeS + "\n" + \
                     "Min Temp: "+ str(minT) + " C\t Time: " + timeS + "\n" + \
                     "Last Temp: "+ str(lastT) + " C\t Time: " + timeS + "\n" + \
                     "Avg Temp: "+ str(avgT) + " C\t Time: " + timeS + "\n" + \
                     "Max Hum: "+ str(maxH) + " % \t Time: " + timeS + "\n" + \
                     "Min Hum: "+ str(minH) + " % \t Time: " + timeS + "\n" + \
                     "Last Hum: "+ str(lastH) + " % \t Time: " + timeS + "\n" + \
                     "Avg Hum: "+ str(avgH) + " % \t Time: " + timeS + "\n\n"
        return message

    def getData(self):
        messageList=[]
        self.maxTempList=[]
        self.minTempList=[]
        self.lastTempList=[]
        self.avgTempList=[]
        self.maxHumList=[]
        self.minHumList=[]
        self.lastHumList=[]
        self.avgHumList=[]
        self.timeStamp=[]
        for i in range(3):
            # Process messages by printing out body
            for msg in self.queue.receive_messages(MaxNumberOfMessages=6):
                # Print out the body of the message
                msgBody = ast.literal_eval(msg.body)
                messageList.append(msgBody)
                # Let the queue know that the message is processed
                #msg.delete()
        if messageList:
            for msg in  messageList:
                self.maxTempList.append(msg["Max"]["Temp"])
                self.minTempList.append(msg["Min"]["Temp"])
                self.lastTempList.append(msg["Last"]["Temp"])
                self.avgTempList.append(msg["Avg"]["Temp"])
                self.maxHumList.append(msg["Max"]["Hum"])
                self.minHumList.append(msg["Min"]["Hum"])
                self.lastHumList.append(msg["Last"]["Hum"])
                self.avgHumList.append(msg["Avg"]["Hum"])
                self.timeStamp.append(msg["Max"]["Time"])
            message=self.getMessage()
            self.valDisplay.setText(_translate("Weather", message, None)) 
        else:
            self.errorDisplay.setText(_translate("Weather", "Couldn't grab data try again", None)) 

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    weatherGui = QtGui.QWidget()
    ui = Ui_Weather()
    ui.setupUi(weatherGui)
    weatherGui.show()
    sys.exit(app.exec_())
