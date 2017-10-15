import sys
import time
import datetime
import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def QT():
    ##### Creating an object for the application ################
    app = QApplication(sys.argv)
    ####### Declaring Tabs ########################################
    tabs = QtGui.QTabWidget()
    tab1 = QtGui.QWidget()
    tab2 = QtGui.QWidget()
    tabs.resize (1500, 1500)
    ####### Setting a Window Title ################################
    tabs.setWindowTitle("Temperature and Humidity")
    ######  Creating Vertical Box layout for tab1  ################
    vBoxlayout = QtGui.QVBoxLayout()
    tab1.setLayout(vBoxlayout)
    ####### Creating Vertical Box Layout for tab2  ################
    vBoxlayout = QtGui.QVBoxLayout()
    tab2.setLayout(vBoxlayout)
    ######## Adding names for tab1 and tab2 ########################
    tabs.addTab(tab1,"Temperature")
    tabs.addTab(tab2,"Humidity")
    ################### Creating buttons for tab1####################
    button1 = QPushButton(tab1)
    button2 = QPushButton(tab1)
    button3 = QPushButton(tab1)
    button4 = QPushButton(tab1)
    button9 = QPushButton(tab1)
    b1 = QPushButton(tab1)
    b2 = QPushButton(tab1)
    b3 = QPushButton(tab1)
    b4 = QPushButton(tab1)

    ################## Names of button1 ###########################
    button1.setText("Last Temp")
    button1.move(100,100)
    b1.setText("Time")
    b1.move(100,200)
    ################### Button 2 #################################
    button2.setText("Max Temp")
    button2.move(200,100)
    b2.setText("Time")
    b2.move(200,200)
    ################## Button 3 #################################
    button3.setText("Min Temp")
    button3.move(300,100)
    b3.setText("Time")
    b3.move(300,200)
    ################## Button 4 #################################
    button4.setText("Average Temp")
    button4.move(400,100)
    b4.setText("Time")
    b4.move(400,200)
    ################## Button 9 #################################
    button9.setText("C to F")
    button9.move(600,200)
    ################### Creating buttons for tab2####################
    button5 = QPushButton(tab2)
    button6 = QPushButton(tab2)
    button7 = QPushButton(tab2)
    button8 = QPushButton(tab2)
    button10 = QPushButton(tab2)
    b5 = QPushButton(tab2)
    b6 = QPushButton(tab2)
    b7 = QPushButton(tab2)
    b8 = QPushButton(tab2)

    ################## Names of button1 ###########################
    button5.setText("Last Humidity")
    button5.move(100,100)
    b5.setText("Time")
    b5.move(100,200)

     ################### Button 2 #################################
    button6.setText("Max Humidity")
    button6.move(200,100)
    b6.setText("Time")
    b6.move(200,200)
    ################## Button 3 #################################
    button7.setText("Min Humidity")
    button7.move(300,100)
    b7.setText("Time")
    b7.move(300,200)
    ################## Button 4 #################################
    button8.setText("Avg Humidity")
    button8.move(400,100)
    b8.setText("Time")
    b8.move(400,200)
    ################## Button 10 #################################
    button10.setText("C to F")
    button10.move(600,200)
    tabs.show()
    sys.exit(app.exec_())

def main():
    QT()

if __name__ == '__main__':
    main()
