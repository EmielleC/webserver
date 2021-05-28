
var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};
var team = 0
var rAF = window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame ||
  window.requestAnimationFrame;

var intervalTimer;
var controlMode = 'absolute';

var values = new Array(4);
var globalSensitivty = 1;

let socket;

function changeTeamButton()
{
	changeTeam()
}

function changeControlButton()
{
	controlMode = document.querySelector('input[name="control"]:checked').value;
	rate = document.getElementById('controlRate').value;
	sensitivity = document.getElementById('sensitivity').value;
	changeControl(sensitivity, rate);
	
}

function restartVideoButton()
{
	resolution = document.querySelector('input[name="resolution"]:checked').value;
	resolutionSplit = resolution.split("x");
	framerate = document.querySelector('input[name="framerate"]:checked').value;
	mode = document.querySelector('input[name="mode"]:checked').value;
	quality = document.getElementById('quality').value;
	
	restartVideo(resolutionSplit[0], resolutionSplit[1], framerate, mode, quality)
	iframe.contentWindow.location.reload(true);
}

function webSocketConnectButton()
{
	webSocketConnect();
}

function stopVideoButton()
{
	message = "s,"
	message += " "
	sendWebsocket(message)
}

function restartVideo(width,height,framerate,mode,quality)
{
	message = "v,"
	message += width
	message += ","
	message += height
	message += ","
	message += framerate
	message += ","
	message += mode
	message += ","
	message += quality
	sendWebsocket(message)
	
}

 

function controlInterval()
{
	scangamepads();
	for (j in controllers) {
		var controller = controllers[j];
		
		let data = new Array(5);
		data[0] = team
		
		if ( controlMode == 'absolute')
		{
			values[0] = controller.axes[0].toFixed(4)
			values[1] = controller.axes[1].toFixed(4)
			values[2] = controller.axes[2].toFixed(4)
			values[3] = controller.axes[3].toFixed(4)
		}
		
		if ( controlMode == 'relative')
		{
			values[0] = values[0] + (controller.axes[0].toFixed(4) * globalSensitivty);
			if( values[0] > 1) values[0] = 1;
			if( values[0] < -1) values[0] = -1;
			values[1] = values[1] + (controller.axes[1].toFixed(4) * globalSensitivty);
			if( values[1] > 1) values[1] = 1;
			if( values[1] < -1) values[1] = -1;
			values[2] = values[2] + (controller.axes[2].toFixed(4) * globalSensitivty);
			if( values[2] > 1) values[2] = 1;
			if( values[2] < -1) values[2] = -1;
			values[3] = values[3] + (controller.axes[3].toFixed(4) * globalSensitivty);
			if( values[3] > 1) values[3] = 1;
			if( values[3] < -1) values[3] = -1;
		}
		
		data[1] = values[3]
		data[2] = values[2]
		data[3] = values[1]
		data[4] = values[0]
 
		sendWebsocket(data)
	
	
  }
}


function changeControl(sensitivity, rate)
{
	globalSensitivty = sensitivity;
	values[0] = 0
	values[1] = 0
	values[2] = 0
	values[3] = 0
	clearInterval(intervalTimer);
	milliRate = 1000 / rate;
	intervalTimer = setInterval(controlInterval, milliRate);
	
}


function sendWebsocket(data)
{
	socket.send(data);
}

function webSocketConnect()
{
	ip = document.getElementById('websocketAddress').value;
	socket = new WebSocket(ip);
}


function sendPost(theUrl, data){
  var url = "192.168.1.136:8000";
  var method = "POST";
  var postData = data;
  
  var shouldBeAsync = true;
  var request = new XMLHttpRequest();
  request.onload = function () {
    var status = request.status;
	var data = request.responseText;
  }
  request.open(method, url, shouldBeAsync);
  request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  request.send(postData);
}

function changeTeam()
{
	if(team == 0)
	{
		team = 1;
	}
	else
	{
		team = 0;
	}
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}


function connecthandler(e) {
  addgamepad(e.gamepad);
}
function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad; var d = document.createElement("div");
  
  //rAF(updateStatus);
}

function disconnecthandler(e) {
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
  var d = document.getElementById("controller" + gamepad.index);
  document.body.removeChild(d);
  delete controllers[gamepad.index];
}

function updateStatus() {
	/*
  scangamepads();
  for (j in controllers) {
    var controller = controllers[j];
	
	let data = new Array(5);
    data[0] = team
    data[1] = controller.axes[0].toFixed(4)
    data[2] = controller.axes[1].toFixed(4)
    data[3] = controller.axes[2].toFixed(4)
    data[4] = controller.axes[3].toFixed(4)
 
  //sendPost("192.168.1.136:8000",data);
	sendWebsocket(data)
	
	
  }
  
 
  
  
  rAF(updateStatus);
  */
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i] && (gamepads[i].index in controllers)) {
      controllers[gamepads[i].index] = gamepads[i];
    }
  }
}

if (haveEvents) {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}
