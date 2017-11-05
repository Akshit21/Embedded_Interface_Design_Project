import boto3

def plotTemp(data):
    pass

def plotHum():
    pass

def getData(self):
    messageList=[]
    for i in range(3):
        # Process messages by printing out body
        for msg in self.queue.receive_messages(MaxNumberOfMessages=10):
            # Print out the body of the message
            print('Hello, {0}'.format(msg.body))
            messageList.append(msg.body)
            # Let the queue know that the message is processed
            #msg.delete()
    return messageList
####################################################
# SERVER.PY FILE
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
                    break
            print("WeatherData:"+str(weatherData))
            if "PlotTemp" in message:
                plotTemp(weatherData)
                self.write_message('OK')
            elif "PlotHum" in message:
                plotTemp(weatherData)
                self.write_message('OK')
            else:
                self.write_message(str(weatherData))

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