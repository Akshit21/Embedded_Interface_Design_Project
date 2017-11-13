# **Communication between 2 RPIs using MQTT, AWS, SQS**


## Details
```
*Server RPI*:
1. Created a GUI using Qt designer 5 and converted to .py file (puic5 QTproject.ui -o main.py)
2. Created a google sheet to use as database to store the sensor values
3. Created a MQTT topic to transfer the values to AWS in json format

### Amazon Web Service:
1. Created a java script file to accept the messages from MQTT
2. Created a Lambda Rule which is invoked as message are recieved
3. The invoked function then computes the avg,max,mean by taking previous values along
   with the last values
4. All the values are passed to the SQS queue

### Client RPI:
1. Implemented a mechanism to grab the data from the SQS queue.
2. The message is then converted to more readable format and displayed on Qt GUI.
3. On button requests graphs are plotted for all the values.
```

## Setup
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
	5. boto3
	6. matplotlib
```

## Prerequisites
```
1. Setup an AWS account
2. Refer AWS documentation to setup AWS - IOT
3. Create a Lambda rule to setup invocation of Lambda Function
4. Create sqs queue and name it myq
```

## Citation 
```
1. Adafruit_DHT and google spread sheet: https://github.com/adafruit/Adafruit_Python_DHT
2. AWS MQTT, Lambda SQS : https://us-west-2.console.aws.amazon.com/iotv2/home?region=us-east-2#/learnHub
```

## Project Tasks Accomplished
```
### Required:
1. Created Server QT interface
2. Used Google sheet to store the values of the sensor output
3. Setup MQTT connection with AWS Cloud
4. Created a Lambda rule to invoke a function to compute mean,max,min of the readings
5. Implemented java script to accept the values from MQTT protocol and perform computation
6. After computation the message is sent to SQS queue
7. Client Rpi setups a connection with AWS and grabs the data from the queue
8. The received data is displayed onto QT window and graph is plotted on button request
   along with the option of converting C to F or vice versa
   
### Extra Credits
1. Implemented CloudWatch to monitor the Data
2. Setup an Alarm to trigger if there are any errors occured for Lambda invocation
3. Used SNS service to notify the user via email
4. Used Dynamodb to store the latest values received by AWS
```

## Run the code
```
1. python3 ServerPi/main.py && python3 ServerPi/server.py
2. node AwsLambda/sqspoll.js
3. python3 ClientPi/clientQt.py
```
