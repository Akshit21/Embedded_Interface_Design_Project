//Reference: http://blog.teamtreehouse.com/an-introduction-to-websockets


window.onload = function() {   
  // Get references to elements on the page.
  var form = document.getElementById('message-form');
  var messageField = document.getElementById('message');
  var textBox = document.getElementById('text_box');
  var socketStatus = document.getElementById('status');
  var closeBtn = document.getElementById('close');
  var avgtempBtn = document.getElementById('avgtemp_button');
  var avghumBtn = document.getElementById('avghum_button');
  var maxtempBtn = document.getElementById('maxtemp_button');
  var mintempBtn = document.getElementById('mintemp_button');
  var lasttempBtn = document.getElementById('lasttemp_button');
  var maxhumBtn = document.getElementById('maxhum_button');
  var minhumBtn = document.getElementById('minhum_button');
  var lasthumBtn = document.getElementById('lasthum_button');
   
  // Create a new WebSocket.
  // (IP Address of the Server Pi is passed as the url)
  var socket = new WebSocket('ws://127.0.1.1:8888/ws');

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
	  textBox.innerHTML = (message+ "\n\n" + currentDateTime);      
  };

  // Show a disconnected message when the WebSocket is closed.
  socket.onclose = function(event) {
    socketStatus.innerHTML = 'Disconnected from WebSocket.';
    socketStatus.className = 'closed';
  };
  
  
  //Handle onclick events for each of the buttons

  avgtempBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "AvgTemp";
	 // Send the message through the WebSocket.
	 socket.send(message);
	 return false;
  };
 
  maxtempBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "MaxTemp";
	 socket.send(message);
	 return false;
  };
 
  mintempBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "MinTemp";
	 socket.send(message);
	 return false;
  };
 
  lasttempBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "LastTemp";
     socket.send(message);
	 return false;
  };
 
  avghumBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "AvgHum";
	 socket.send(message);
	 return false;
  };
 
  maxhumBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "MaxHum";
	 socket.send(message);
	 return false;
  };
 
  minhumBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "MinHum";
	 socket.send(message);
	 return false;
  };
 
  lasthumBtn.onclick = function(e) {
	 e.preventDefault();
	 var message = "LastHum";
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
