// Load the AWS SDK for Node.js
var AWS = require('./aws-sdk');
// Load credentials and set the region from the JSON file
AWS.config.loadFromPath('./config.json');

// Create an SQS service object
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});
var tempValue = 22.5;
var params = {
 DelaySeconds: 1,
 /*MessageAttributes: {
  "Title": {
    DataType: "String",
    StringValue: "Temperature"
   },
  "Author": {
    DataType: "String",
    StringValue: "John Grisham"
   },
  "WeeksOn": {
    DataType: "Number",
    StringValue: "6"
   }
 },*/
 MessageBody: "Temperature Value: " + tempValue.toString(),
 QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/SQS_QUEUE_NAME" // Que URl will change based on our queue
};

sqs.sendMessage(params, function(err, data) {
  if (err) {
    console.log("Error", err);
  } else {
    console.log("Success", data.MessageId);
  }
});