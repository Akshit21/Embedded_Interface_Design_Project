import sys
import time
import datetime
import Adafruit_DHT
import gspread
from collections import defaultdict
from oauth2client.service_account import ServiceAccountCredentials
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from db_update import db

def QT():
    global t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18
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
    t1.move(300,150)
    t1.resize(250,60)
    t2 = QLabel(tab1)
    t2.move(300,350)
    t2.resize(250,60)
    t3 = QLabel(tab1)
    t3.move(500,150)
    t3.resize(250,60)
    t4 = QLabel(tab1)
    t4.move(500,350)
    t4.resize(250,60)
    t5 = QLabel(tab1)
    t5.move(700,150)
    t5.resize(250,60)
    t6 = QLabel(tab1)
    t6.move(700,350)
    t6.resize(250,60)
    t7 = QLabel(tab1)
    t7.move(900,150)
    t7.resize(250,60)
    t8 = QLabel(tab1)
    t8.move(900,350)
    t8.resize(250,60)
    t9 = QLabel(tab1)
    t9.move(1200,300)
    t9.resize(250,60)
    #################    Creating labels for tab2 #####################
    t10 = QLabel(tab2)
    t10.move(300,150)
    t10.resize(250,60)
    t11 = QLabel(tab2)
    t11.move(300,350)
    t11.resize(250,60)
    t12 = QLabel(tab2)
    t12.move(500,150)
    t12.resize(250,60)
    t13 = QLabel(tab2)
    t13.move(500,350)
    t13.resize(250,60)
    t14 = QLabel(tab2)
    t14.move(700,150)
    t14.resize(250,60)
    t15 = QLabel(tab2)
    t15.move(700,350)
    t15.resize(250,60)
    t16 = QLabel(tab2)
    t16.move(900,150)
    t16.resize(250,60)
    t17 = QLabel(tab2)
    t17.move(900,350)
    t17.resize(250,60)
    t18 = QLabel(tab2)
    t18.move(1200,300)
    t18.resize(250,60)
    ################## Names of button1 ###########################
    button1.setText("Last Temp")
    button1.move(300,100)
    b1.setText("Last Time")
    b1.move(300,300)
    ################### Button 2 #################################
    button2.setText("Max Temp")
    button2.move(500,100)
    b2.setText(" Max Time")
    b2.move(500,300)
    ################## Button 3 #################################
    button3.setText("Min Temp")
    button3.move(700,100)
    b3.setText("Min Time")
    b3.move(700,300)
    ################## Button 4 #################################
    button4.setText("Average Temp")
    button4.move(900,100)
    b4.setText(" Avg Time")
    b4.move(900,300)
    ################## Button 9 #################################
    button9.setText("C to F")
    button9.move(1200,200)
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
    button5.move(300,100)
    b5.setText("Last Time")
    b5.move(300,300)
    ################### Button 2 #################################
    button6.setText("Max Humidity")
    button6.move(500,100)
    b6.setText("Max Time")
    b6.move(500,300)
    ################## Button 3 #################################
    button7.setText("Min Humidity")
    button7.move(700,100)
    b7.setText("Min Time")
    b7.move(700,300)
    ################## Button 4 #################################
    button8.setText("Avg Humidity")
    button8.move(900,100)
    b8.setText("Avg Time")
    b8.move(900,300)
    ################## Button 10 #################################
    button10.setText("C to F")
    button10.move(1200,200)
    ############## Defining actions for buttons ##################
    button1.clicked.connect(button1_clicked)
    button2.clicked.connect(button2_clicked)
    button3.clicked.connect(button3_clicked)
    button4.clicked.connect(button4_clicked)
    button5.clicked.connect(button5_clicked)
    button6.clicked.connect(button6_clicked)
    button7.clicked.connect(button7_clicked)
    button8.clicked.connect(button8_clicked)
    button9.clicked.connect(button9_clicked)
    button10.clicked.connect(button10_clicked)
    b1.clicked.connect(b1_clicked)
    b2.clicked.connect(b2_clicked)
    b3.clicked.connect(b3_clicked)
    b4.clicked.connect(b4_clicked)
    b5.clicked.connect(b5_clicked)
    b6.clicked.connect(b6_clicked)
    b7.clicked.connect(b7_clicked)
    b8.clicked.connect(b8_clicked)
    tabs.show()
    sys.exit(app.exec_())

def button1_clicked():
    print('Button1 is clicked')
    q = db()
    weatherData = q.login_open_sheet('eidproject.json','EID')
    t1.setText(str(weatherData['Last']['Temp']))
    print('Display')
def button2_clicked():
    print('Button2 is clicked')
    q = db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t3.setText(str(weatherData['Max']['Temp']))
def button3_clicked():
    print('Button3 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t5.setText(str(weatherData['Min']['Temp']))
def button4_clicked():
    print('Button4 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t7.setText(str(weatherData['Avg']['Temp']))
def button5_clicked():
    print('Button5 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t10.setText(str(weatherData['Last']['Hum']))
def button6_clicked():
    print('Button6 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t12.setText(str(weatherData['Max']['Hum']))
def button7_clicked():
    print('Button7 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t14.setText(str(weatherData['Min']['Hum']))
def button8_clicked():
    print('Button8 is clicked')
    q = db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t16.setText(str(weatherData['Avg']['Hum']))
def button9_clicked():
    print('Button9 is clicked')
    q =db()
    weatherData = q.login_open_sheet('eidproject.json','EID')
    farenheit1 = ((9.0/5.0) * (float(weatherData['Last']['Temp']))) + 32.0
    farenheit2 = ((9.0/5.0) * (float(weatherData['Max']['Temp']))) + 32.0
    farenheit3 = ((9.0/5.0) * (float(weatherData['Min']['Temp']))) + 32.0
    farenheit4 = ((9.0/5.0) * (float(weatherData['Avg']['Temp']))) + 32.0
    t1.setText(str(farenheit1))
    t3.setText(str(farenheit2))
    t5.setText(str(farenheit3))
    t7.setText(str(farenheit4))
def button10_clicked():
    print('Button10 is clicked')
    q =db()
    weatherData = q.login_open_sheet('eidproject.json','EID')
    farenheit1 = ((9.0/5.0) * (float(weatherData['Last']['Hum']))) + 32.0
    farenheit2 = ((9.0/5.0) * (float(weatherData['Max']['Hum']))) + 32.0
    farenheit3 = ((9.0/5.0) * (float(weatherData['Min']['Hum']))) + 32.0
    farenheit4 = ((9.0/5.0) * (float(weatherData['Avg']['Hum']))) + 32.0
    t10.setText(str(farenheit1))
    t12.setText(str(farenheit2))
    t14.setText(str(farenheit3))
    t16.setText(str(farenheit4))


def b1_clicked():
    print('b1 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t2.setText(str(weatherData['Last']['Time']))
def b2_clicked():
    print('b2 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t4.setText(str(weatherData['Max']['Time']))
def b3_clicked():
    print('b3 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t6.setText(str(weatherData['Min']['Time']))
def b4_clicked():
    print('b4 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t8.setText(str(weatherData['Avg']['Time']))
def b5_clicked():
    print('b5 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t11.setText(str(weatherData['Last']['Time']))
def b6_clicked():
    print('b6 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t13.setText(str(weatherData['Max']['Time']))
def b7_clicked():
    print('b7 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t15.setText(str(weatherData['Min']['Time']))
def b8_clicked():
    print('b8 is clicked')
    q =db()
    weatherData =q.login_open_sheet('eidproject.json','EID')
    t17.setText(str(weatherData['Avg']['Time']))


def main():
    QT()

if __name__ == '__main__':
    main()
