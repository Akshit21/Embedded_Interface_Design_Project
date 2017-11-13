// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');

exports.handler = function (event, context){
    
        
    
    // Create an SQS service object
    var sqs = new AWS.SQS({apiVersion: '2012-11-05'});
    // checks if count is 1 and initialises the sqs with temperature and humidity values
    if(event.count == 1)
    {
        
        var params1 = {
         DelaySeconds: 0,
         MessageBody: "{ \"temp\": " + event.temp +", " + " \"avg_temp\": " + event.temp + "," + "\"max_temp\": " + event.temp + "," + "\"min_temp\": " + event.temp + "," +"\"humidity\": " + event.humidity + "," + "\"avg_humidity\": " + event.humidity + "," + "\"max_humidity\": " + event.humidity + "," + "\"min_humidity\": " + event.humidity + "}",
         QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/statq"
        };
	// sends message to sqs 	
    sqs.sendMessage(params1, function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
        console.log("Its successful", data.MessageId);
      }
    });
    }
    else
    {
    
        
            var receiveparams = {
         AttributeNames: [
            "SentTimestamp"
         ],
         MaxNumberOfMessages: 1,
         MessageAttributeNames: [
            "All"
         ],
         QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/statq",
         VisibilityTimeout: 0,
         WaitTimeSeconds: 0
        };


		// receives messages from the sqs for updating the statistics
        sqs.receiveMessage(receiveparams, function(err, data) {
          if (err) {
            console.log("Receive Error", err);
          } else if (data.Messages) 
          { // parsing the json message for getting float values from the message
            var parse_object = JSON.parse(data.Messages[0].Body)  
            // calculation to find the running average
            var avg_temp = (((parse_object.avg_temp * (event.count - 1))+ event.temp)/event.count);
            avg_temp=Number((avg_temp).toFixed(2));
            var avg_humidity = (((parse_object.avg_humidity * (event.count - 1))+ event.humidity)/event.count);
            avg_humidity=Number(avg_humidity.toFixed(2));
            var min_temp;
            var min_humidity;
            var max_temp;
            var max_humidity;

            //checking the current statistical measures with the previous ones to modify in the sqs
            if(event.temp < parse_object.min_temp)
            {
                min_temp = event.temp;    
            }
            else
            {
                min_temp = parse_object.min_temp;
            }
            
            if(event.humidity < parse_object.min_humidity)
            {
                min_humidity = event.humidity;
            }
            else
            {
                min_humidity = parse_object.min_humidity;
            }
            
            if(event.temp > parse_object.max_temp)
            {
                max_temp = event.temp; 
            }
            else
            {
                max_temp = parse_object.max_temp;
            }

            if(event.humidity > parse_object.max_humidity)
            {
                max_humidity = event.humidity;
            }
            else
            {
                max_humidity = parse_object.max_humidity;
            }
            
            console.log("Message - ", data.Messages[0].Body);  
            var deleteParams = {
              QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/statq",
              ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            // deleting the message from the sqs 
            sqs.deleteMessage(deleteParams, function(err, data) {
              if (err) {
                console.log("Delete Error", err);
              } else {
                console.log("Message Deleted", data);
              }
            });
                var params2 = {
                DelaySeconds: 0,
                MessageBody: "{ \"temp\": " + event.temp +", " + " \"avg_temp\": " + avg_temp + "," + "\"max_temp\": " + max_temp + "," + "\"min_temp\": " + min_temp + ",\n" +"\"humidity\": " + event.humidity + "," + "\"avg_humidity\": " + avg_humidity + "," + "\"max_humidity\": " + max_humidity + "," + "\"min_humidity\": " + min_humidity + "}",
                QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/statq"
                };        
                
                var params3 = {
                DelaySeconds: 0,
                MessageBody: "{ \"temp\": " + event.temp +", " + " \"avg_temp\": " + avg_temp + "," + "\"max_temp\": " + max_temp + "," + "\"min_temp\": " + min_temp + ",\n" +"\"humidity\": " + event.humidity + "," + "\"avg_humidity\": " + avg_humidity + "," + "\"max_humidity\": " + max_humidity + "," + "\"min_humidity\": " + min_humidity + "}",
                QueueUrl: "https://sqs.us-east-2.amazonaws.com/291619158901/myq"
                };        
				//populating the sqs with new values
                sqs.sendMessage(params2, function(err, data) {
                if (err) {
                console.log("Error", err);
                } else {
                console.log("Its successful", data.MessageId);
                }
                });  

                sqs.sendMessage(params3, function(err, data) {
                if (err) {
                console.log("Error", err);
                } else {
                console.log("Its successful", data.MessageId);
                }
                });  
                
          }
        });

    
    
    
    }
    

    
};