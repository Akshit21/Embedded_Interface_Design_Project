"""
# Weather Monitorting GUI

# Platform : Raspberry Pi 3
# Programming language: Python 2.7
# Sensor:  Adafruit 2302 Temperature Sensor

# Software requirements:
*Install QT Designer 4 or 5, #4 if using Python 2.7
*Install python modules :
	1 .matplotlib
	2. PyQt4
	3. numpy
*Download Adafruit_DHT library from https://github.com/adafruit/Adafruit_Python_DHT

# Citation: getTemp and getHumidity taken from the above link
			Adafruit_DHT drivers taken from the above link
		
# Created a gui using Qt designer and converted to .pyplot

# This GUI performs following tasks

	$$ Get Temperature
	$$ Get Humidity
	$$ Average of temperature/humidity over time
	$$ Alarm if temperature goes above threshold
	$$ Plot graph for temp/humidity over time

# Run the code: python eid1.py
"""
# -*- coding: utf-8 -*-
#
# weatherGui implementation generated from reading ui file 'Project1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#

# Python imports
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import numpy as np
import time

# Adafruit library imports
import Adafruit_DHT
from Adafruit_DHT import common
from Adafruit_DHT import Raspberry_Pi_2_Driver as driver

# *******************************************************************************

__author__ = "Akshit Shah"
__copyright__ = "Copyright (C) 2017 by Akshit Shah"
#
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. Users are
# permitted to modify this and use it to learn about the field of embedded
# software. Akshit Shah, and the University of Colorado
# are not liable for any misuse of this material.


# *******************************************************************************

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

class Ui_Weather(QtGui.QWidget):

	# class initialization
    def __init__(self):
        super(Ui_Weather,self).__init__()
        self.setupUi(self)
        self.editLine = QtGui.QLineEdit()
		
		# variables for recording values for graph and avg
        self.tempList=[]
        self.humidityList=[]
        self.tempTimeList=[]
        self.humidityTimeList=[]
        
	# GUI setup=> defining button, text editor properties	
    def setupUi(self, Weather):
		Weather.setObjectName(_fromUtf8("Weather"))
        Weather.resize(639, 479)
        Weather.setStyleSheet(_fromUtf8("background-color: rgb(85, 255, 255);\n"
"background: url(/home/pi/QtProject/various-weather.jpg);"))
        
		self.quitButton = QtGui.QPushButton(Weather)
        self.quitButton.setGeometry(QtCore.QRect(480, 400, 121, 41))
        self.quitButton.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        
		self.tempButton = QtGui.QPushButton(Weather)
        self.tempButton.setGeometry(QtCore.QRect(60, 40, 231, 41))
        self.tempButton.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.tempButton.setObjectName(_fromUtf8("tempButton"))
        
		self.humidityButton = QtGui.QPushButton(Weather)
        self.humidityButton.setGeometry(QtCore.QRect(370, 40, 221, 41))
        self.humidityButton.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.humidityButton.setObjectName(_fromUtf8("humidityButton"))
        
		self.setAlarm = QtGui.QPushButton(Weather)
        self.setAlarm.setGeometry(QtCore.QRect(40, 170, 131, 28))
        self.setAlarm.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.setAlarm.setObjectName(_fromUtf8("setAlarm"))
        
		self.plotGraph = QtGui.QPushButton(Weather)
        self.plotGraph.setGeometry(QtCore.QRect(250, 170, 141, 28))
        self.plotGraph.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.plotGraph.setObjectName(_fromUtf8("plotGraph"))
        
		self.avgValue = QtGui.QPushButton(Weather)
        self.avgValue.setGeometry(QtCore.QRect(480, 170, 131, 28))
        self.avgValue.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.avgValue.setObjectName(_fromUtf8("avgValue"))
        
		self.textEditObj = QtGui.QTextEdit(Weather)
        self.textEditObj.setGeometry(QtCore.QRect(50, 340, 261, 87))
        self.textEditObj.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(85, 255, 255);"))
        self.textEditObj.setObjectName(_fromUtf8("textEditObj"))
        
		self.quitButton.raise_()
        self.humidityButton.raise_()
        self.tempButton.raise_()
        self.setAlarm.raise_()
        self.plotGraph.raise_()
        self.avgValue.raise_()
        self.textEditObj.raise_()

        self.retranslateUi(Weather)
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Weather.close)
        QtCore.QMetaObject.connectSlotsByName(Weather)

    def retranslateUi(self, Weather):
		# Set text and tool tip
        Weather.setWindowTitle(_translate("Weather", "Weather", None))
        self.quitButton.setText(_translate("Weather", "Quit", None))
        self.tempButton.setToolTip(_translate("Weather", "<html><head/><body><p>Current Temperature</p></body></html>", None))
        self.tempButton.setText(_translate("Weather", "Get Temperature", None))
        self.humidityButton.setToolTip(_translate("Weather", "<html><head/><body><p>Current Humidity</p></body></html>", None))
        self.humidityButton.setText(_translate("Weather", "Get Humidity", None))
        self.setAlarm.setToolTip(_translate("Weather", "<html><head/><body><p>Set Alarm for monitoring temperature/humidity</p></body></html>", None))
        self.setAlarm.setText(_translate("Weather", "Alarm", None))
        self.plotGraph.setToolTip(_translate("Weather", "<html><head/><body><p>Plot graph for temp/humidity vs time</p></body></html>", None))
        self.plotGraph.setText(_translate("Weather", "Graph", None))
        self.avgValue.setToolTip(_translate("Weather", "<html><head/><body><p>Average of temp/humidity valules over time</p></body></html>", None))
        self.avgValue.setText(_translate("Weather", "Average", None))
		
		# Perform tasks if button clicked
        self.tempButton.clicked.connect(self.getTemp)
        self.humidityButton.clicked.connect(self.getHumidity)
        self.avgValue.clicked.connect(self.getAvg)
        self.setAlarm.clicked.connect(self.setAlarmValue)
        self.plotGraph.clicked.connect(self.plotGraphData)
        
    def getTemp(self):
        # Get a reading from C driver code.
        self.result, self.humidity, self.temp = driver.read(22, 4)
        
        # Error Handling
        if self.result in common.TRANSIENT_ERRORS:
            # Signal no result could be obtained, but the caller can retry.
            return (None, None)
        elif self.result == common.DHT_ERROR_GPIO:
            raise RuntimeError('Error accessing GPIO.')
        elif self.result != common.DHT_SUCCESS:
            # Some kind of error occured.
            raise RuntimeError('Error calling DHT test driver read: {0}'.format(self.result))
        
        #Append values in respective lists for history/graph
        self.tempList.append(self.temp)
        self.time=time.time()
        self.tempTimeList.append(self.time)
        
        # Display the data in the text editor
		self.textEditObj.setText(_translate("Weather", "Temp: {0:.2f}  C".format(self.temp)+\
                                            "\nTime:"+datetime.now().strftime('%H:%M:%S'), None))
    
    def getHumidity(self):
        # Get a reading from C driver code.
        self.result, self.humidity, self.temp = driver.read(22, 4)
        
        # Error Handling
        if self.result in common.TRANSIENT_ERRORS:
            # Signal no result could be obtained, but the caller can retry.
            return (None, None)
        elif self.result == common.DHT_ERROR_GPIO:
            raise RuntimeError('Error accessing GPIO.')
        elif self.result != common.DHT_SUCCESS:
            # Some kind of error occured.
            raise RuntimeError('Error calling DHT test driver read: {0}'.format(self.result))
        
        #Append values in respective lists for history/graph
        self.humidityList.append(self.humidity)
        self.time=time.time()
        self.humidityTimeList.append(self.time)
        
        # Display the data in the text editor
		self.textEditObj.setText(_translate("Weather", "Humidity: {0:.2f} %".format(self.humidity)+\
                                            "\nTime:"+datetime.now().strftime('%H:%M:%S'), None))
    
    def getAvg(self):
		# check if any values are recorded or not
        if not self.tempList or not self.humidityList:
            self.textEditObj.setText(_translate("Weather", "No Current Data\nGather some values\nClick on Get Temperature and Get Humidity", None))
        else:
            self.textEditObj.setText(_translate("Weather", "Average Temp: {0:.2f}  C".format(np.mean(self.tempList))+\
                                            "\nAverage Humidity: {0:.2f} %".format(np.mean(self.humidityList)), None))
    
    def setAlarmValue(self):
        flag=False
        try:
			# take input from the user 
            myList=str(self.textEditObj.toPlainText())
            myList=myList.split(',')
            self.variable = float(myList[0]) # threshold temp
            self.timerVal=int(myList[1]) # alarm time to wait
            flag=True
        except ValueError:
            self.textEditObj.setText(_translate("Weather", "Invalid Value, Enter a valid temp and time\nFormat Temp, Time(secs)", None))
        if flag:
			# loop till time is completed
            while self.timerVal:
                self.timerVal-=1
				# check if temp crosses the threshold
                if self.variable >= self.temp:
					# if threshold limit reached play alarm and display the alert
                    self.textEditObj.setText(_translate("Weather", "High Temperature Alert !!!", None))
                    QtGui.QSound("/home/pi/QtProject/alarm.mp3").play()
                time.sleep(1)
                
    def plotGraphData(self):
		# Graph plotting
        plt.subplot(2,1,1)
        plt.plot(self.tempTimeList,self.tempList)
        plt.xlabel('Time (sec)')
        plt.ylabel('Temp (C)')
        plt.title('Temperature Variance')
        plt.subplot(2,1,2)
        plt.plot(self.humidityTimeList,self.humidityList)
        plt.xlabel('Time (sec)')
        plt.ylabel('Humidity (%)')
        plt.title('Humidity Variance')
        plt.tight_layout()
        plt.show()
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    weatherGui = QtGui.QWidget()
    ui = Ui_Weather()
    ui.setupUi(weatherGui)
    weatherGui.show()
    sys.exit(app.exec_())