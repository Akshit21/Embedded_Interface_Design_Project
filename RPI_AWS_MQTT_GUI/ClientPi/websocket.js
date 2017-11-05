//Reference: http://blog.teamtreehouse.com/an-introduction-to-websockets


window.onload = function() {   
  // Get references to elements on the page.
  var form = document.getElementById('message-form');
  var messageField = document.getElementById('message');
  var textBox = document.getElementById('text_box');
  var socketStatus = document.getElementById('status');
  var closeBtn = document.getElementById('close');
  var getValBtn = document.getElementById('getVal_button');
  var plotTempBtn = document.getElementById('plotTemp_button');
  var plotHumBtn = document.getElementById('plotHum_button');

  var tempFlag = false;
  var humFlag = false;
   
  // Create a new WebSocket.
  // (IP Address of the Server Pi is passed as the url)
  var socket = new WebSocket('ws://10.0.0.17:8888/ws');

  // Handle and log any errors that occur.
  socket.onerror = function(error) {
    console.log('WebSocket Error: ' + error);
	textBox.innerHTML = ("WebSocket Error: " + error);
  };
  
  // Show a connected message when the WebSocket is opened.
  socket.onopen = function(event) {
    socketStatus.innerHTML = 'Connected to: ' + event.currentTarget.url;
    socketStatus.className = 'open';
  };

  // Display messages sent by the server alongwith the timestamp.
  socket.onmessage = function(event) {
	  var message = event.data;
	  var currentDateTime = new Date();
	  if (message == "OK" && tempFlag){
		window.location.replace("10.0.0.17:8888/temp.png")
	  }
	  else if (message == "OK" && humFlag){
		window.open("10.0.0.17:8888/hum.png","_self")
	  }
	  else{
	  	textBox.innerHTML = (message+ "\n\n" + currentDateTime);
	  }      
  };

  // Show a disconnected message when the WebSocket is closed.
  socket.onclose = function(event) {
    socketStatus.innerHTML = 'Disconnected from WebSocket.';
    socketStatus.className = 'closed';
  };
  
  
  //Handle onclick events for each of the buttons
  getValBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "GetVal";
	 humFlag = false;
	 tempFlag = false;
	 // Send the message through the WebSocket.
	 socket.send(message);
	 return false;
  };
 
  plotTempBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "PlotTemp";
	 tempFlag = true;
	 humFlag = false;
	 socket.send(message);
	 return false;
  };
 
  plotHumBtnonclick = function(e) {
	 e.preventDefault();
	 var message = "PlotHum";
	 humFlag = true;
	 tempFlag = false;
	 socket.send(message);
	 return false;
  };
 
 
  // Close the WebSocket connection when the close button is clicked.
  closeBtn.onclick = function(e) {
    e.preventDefault();
    // Close the WebSocket.
    socket.close();
    return false;
  };
  
};
