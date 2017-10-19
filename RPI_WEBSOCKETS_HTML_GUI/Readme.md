# **Communicate between 2 RPIs using Tornodo WebSockets**



## Details
```
### Server Rpi:
1. Created a GUI using Qt designer 5 and converted to .py file (puic4 QTproject.ui -o eid1.py)
2. Created a google sheet and use as database to store the sensor values
3. Created a websocket server using python and tornodo to host another rpi

### Client Rpi
1. Created a websocket using javascript client to receive data from host
2. Created Html based web page to display all the received data
3. Used javascript
```

### Platform : Raspberry Pi 3
### Programming language: Python 3.5.3
### Sensor:  Adafruit 2302 Temperature Sensor (Connect to GPIO 4 of Rpi)
### Software requirements:
1. Install QT Designer 5
2. Install python modules :
	1. Tornodo
	2. PyQt4
	3. oauth2client
	4. gspread
3. Clone the git repository https://github.com/Akshit21/QTProject

### Citation: 
```
Adafruit_DHT and google spread sheet: https://github.com/adafruit/Adafruit_Python_DHT
Websocket: http://blog.teamtreehouse.com/an-introduction-to-websockets
			: https://os.mbed.com/cookbook/Websockets-Server 
```

### Folder contents
1. Adafruit_DHT ==> Drivers for Temp Sensor
2. main.py ==> Main file of the project which contains GUI, storing in database and google sheet authentication code
3. server.py ==> Server file which creates a websocket server, grabs data from database and sends it to client upon request
4. googleSheetAuth.json ==> Google Sheet authentication information
5. websocket.js ==> websocket javascript for client to run websocket and ping server for data
6. websocketWeb.html ==> web page gui
7. Readme.md

## This GUI has below capabilities
  ### *Required*:
	@Todo
  
  ### *Extra Credits*:
	@Todo
	
## Run the code 
```
1. python3 main.py && python3 server.py
2. open websocketWeb
```

