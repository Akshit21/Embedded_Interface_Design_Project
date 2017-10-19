# **A GUI for Weather monitoring system**



## Details
### Created a GUI using Qt designer 5 and converted to .py file (puic4 QTproject.ui -o eid1.py)

### Platform : Raspberry Pi 3
### Programming language: Python 3.5.3
### Sensor:  Adafruit 2302 Temperature Sensor (Connect to GPIO 4 of Rpi)
### Software requirements:
1. Install QT Designer 5
2. Install python modules :
	1. Matplotlib
	2. PyQt4
	3. Numpy
3. Clone the git repository https://github.com/Akshit21/QTProject

### Citation: Adafruit_DHT library from https://github.com/adafruit/Adafruit_Python_DHT

### Folder contents
1. Adafruit_DHT ==> Drivers for Temp Sensor
2. eid1.py ==> Main file of the project which on running creates a GUI (static graph)
3. eid2.py ==> Main file of the project which on running creates a GUI (dynamic graph)
4. various-weather.jpg ==> background image of the GUI
5. alarm.mp3 ==> audio for alarm
6. Readme.md

## This GUI has below capabilities
  ### *Required*:
	* Get Temperature value with time of request
	* Get Humidity value with time of request
  
  ### *Extra Credits*:
	* Average of temperature/humidity over time
	* Alarm if temperature goes above threshold (display and sound)
	* Plot graph for temp/humidity over time (static and dynamic)
	* Tool tips for showing user what will the GUI do if a particular button is pressed
	
## Run the code: python3 eid1.py 
*Make sure to change the path in eid1.py for weather background and alarm according to your directory*
