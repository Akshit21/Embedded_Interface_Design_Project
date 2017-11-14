var awsIot = require('aws-iot-device-sdk');

//
// Replace the values of '<YourUniqueClientIdentifier>' and '<YourCustomEndpoint>'
// with a unique client identifier and custom host endpoint provided in AWS IoT cloud
// NOTE: client identifiers must be unique within your AWS account; if a client attempts 
// to connect with a client identifier which is already in use, the existing 
// connection will be terminated.
//
var device = awsIot.device({
   keyPath: "/home/pi/EID/Embedded_Interface_Design_Project/RPI_AWS_MQTT_GUI/ServerPi/cert/f224d37fff-private.pem.key",
  certPath: "/home/pi/EID/Embedded_Interface_Design_Project/RPI_AWS_MQTT_GUI/ServerPi/cert/f224d37fff-certificate.pem.crt",
    caPath: "/home/pi/EID/Embedded_Interface_Design_Project/RPI_AWS_MQTT_GUI/ServerPi/cert/rootCA.pem",
  clientId: "MyRaspberryPi",
      host: "a1had6bfve7jzo.iot.us-east-2.amazonaws.com"
});
var global_message;
//
// Device is an instance returned by mqtt.Client(), see mqtt.js for full
// documentation.
//
device
  .on('connect', function() {
    console.log('connect');
    device.subscribe('WeatherData');
    //device.publish('topic_2', JSON.stringify({ test_data: 1}));
  });

device
  .on('message', function(topic, payload) {
    global_message=payload;
	console.log('message', topic, payload);
  });


// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
// Load credentials and set the region from the JSON file
AWS.config.loadFromPath('./config.json');

// Create an SQS service object
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

var params = {
 MessageAttributes: {
  "weatherdata": {
    DataType: "String",
    StringValue=global_message,
   },
 QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/Weather.fifo"
};

sqs.sendMessage(params, function(err, data) {
  if (err) {
    console.log("Error", err);
  } else {
    console.log("Success", data.MessageId);
  }
});