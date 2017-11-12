import boto3
import ast
import itertools
import matplotlib
import matplotlib.pyplot as plt
import datetime
# importing required libraries
#plotting temperature values
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
    plt.savefig('temp.png',bbox_inches='tight')
# plotting humidity values
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
    plt.savefig('hum.png',bbox_inches='tight')
#getting message from sqs
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
        return getMessage(self)
    return messageList

####################################################
# CLIENT.PY FILE
####################################################
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes.
'''
# Creating class handlers
class WSHandler(tornado.websocket.WebSocketHandler):
    # Open Worksheet
    def open(self):
        print ('new connection')
        # Get the service resource
        self.sqs = boto3.resource('sqs')
        # Get the queue
        self.queue = self.sqs.get_queue_by_name(QueueName='Weather.fifo')
        
    #  Receiving messages from client
    def on_message(self, message):
        print ('message received:  %s' % message)
        if "login" in message:
            validate=message.split(" ")
            if validate[1]== 'Weather' and validate[2]=='Rpi3':
                self.write_message('OK')
            else:
                self.write_message('NOT')
        else:
            while True:
                weatherData = getData(self)
                if not weatherData:
                    self.write_message('Error in collecting data from SQS!! Trying Again.')
                else:
                    self.write_message('Received correct data.')
                    break
            print("**************Weather Analysis**************\n"+weatherData)
            if "PlotTemp" in message:
                plotTemp(self)
                self.write_message('OK')
            elif "PlotHum" in message:
                plotTemp(self)
                self.write_message('OK')
            else:
                self.write_message(weatherData)

    # Closing the client connection
    def on_close(self):
        print ('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r"/(temp.png)", tornado.web.StaticFileHandler, {'path':'./'}),
    (r"/(hum.png)", tornado.web.StaticFileHandler, {'path':'./'})
])

if __name__ == "__main__":
    ######## STARTING TORNADO WEBSERVER SOCKET
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()