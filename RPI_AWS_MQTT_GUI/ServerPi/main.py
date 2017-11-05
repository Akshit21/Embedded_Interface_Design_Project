import json
import sys
import time
import datetime
import matplotlib.pyplot as plt
import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
        #plt.show()
        plt.savefig('graph.png',bbox_inches='tight')
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
    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    weatherGui = QtGui.QWidget()
    ui = Ui_Weather()
    ui.setupUi(weatherGui)
    weatherGui.show()
    sys.exit(app.exec_())
