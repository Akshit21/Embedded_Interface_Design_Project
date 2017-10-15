import sys
import time
import datetime
import Adafruit_DHT
import gspread
import json
from server import *
from collections import defaultdict
from oauth2client.service_account import ServiceAccountCredentials
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def QT():
    global t1
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
    ################## Creating labels for tab1 ###################
    t1 = QLabel(tab1)
    t1.move(100,150)
    t1.resize(250,60)
    t2 = QLabel(tab1)
    t2.move(100,250)
    t2.resize(250,60)
    t3 = QLabel(tab1)
    t3.move(200,150)
    t3.resize(250,60)
    t4 = QLabel(tab1)
    t4.move(200,250)
    t4.resize(250,60)
    t5 = QLabel(tab1)
    t5.move(300,150)
    t5.resize(250,60)
    t6 = QLabel(tab1)
    t6.move(300,250)
    t6.resize(250,60)
    t7 = QLabel(tab1)
    t7.move(400,150)
    t7.resize(250,60)
    t8 = QLabel(tab1)
    t8.move(400,250)
    t8.resize(250,60)
    t9 = QLabel(tab1)
    t9.move(600,350)
    t9.resize(250,60)
    #################    Creating labels for tab2 #####################
    t10 = QLabel(tab2)
    t10.move(100,150)
    t10.resize(250,60)
    t11 = QLabel(tab2)
    t11.move(100,250)
    t11.resize(250,60)
    t12 = QLabel(tab2)
    t12.move(200,150)
    t12.resize(250,60)
    t13 = QLabel(tab2)
    t13.move(200,250)
    t13.resize(250,60)
    t14 = QLabel(tab2)
    t14.move(300,150)
    t14.resize(250,60)
    t15 = QLabel(tab2)
    t15.move(300,250)
    t15.resize(250,60)
    t16 = QLabel(tab2)
    t16.move(400,150)
    t16.resize(250,60)
    t17 = QLabel(tab2)
    t17.move(400,250)
    t17.resize(250,60)
    t18 = QLabel(tab2)
    t18.move(600,350)
    t18.resize(250,60)
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
    
def main():
    QT()

if __name__ == '__main__':
    main()
