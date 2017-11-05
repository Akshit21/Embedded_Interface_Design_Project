
$(document).ready(function () {
  var ws;
  ws = new WebSocket("ws://10.0.0.17:8888/ws")

  ws.onmessage = function(evt) {
    // if message received is OK
    if(evt.data == "OK"){
      window.location.replace("weatherWeb.html");
    }
    else{
          alert("Invalid Username or Password")
    }
  };

  $("#login").click(function(evt) {
    // get user entered username and password
    var username =document.getElementById("username").value;
    var password = document.getElementById("password").value;
    // send the username and password to server for validation
    ws.send("login"+" "+username +" " + password)
  });
});
