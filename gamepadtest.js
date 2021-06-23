var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;

var controllers = {};

var team = 0

var intervalTimer;

var values = new Array(4);

var controlMode = 'absolute';
var globalSensitivty = 1;

var socket;

window.onload = function() {
  reloadVideoIframe();
};

function changeTeamButton()
{
	teamToChangeTo = document.querySelector('input[name="team"]:checked').value;
	changeTeam(teamToChangeTo);
}

function changeControlButton()
{
	controlMode = document.querySelector('input[name="control"]:checked').value;
	rate = document.getElementById('controlRate').value;
	sensitivity = document.getElementById('sensitivity').value;
	changeControl(sensitivity, rate);
	
}

function reloadVideoIframe()
{
	var rand = Math.floor((Math.random()*1000000)+1);
	var iframe = document.getElementById('videoFeed');
	var newSource = "http://" + location.hostname + ":8080/?action=stream?uid="+rand;

	iframe.src = newSource;
	iframe.contentWindow.location.reload(true);
	
}

function startVideoButton()
{
	resolution = document.querySelector('input[name="resolution"]:checked').value;
	resolutionSplit = resolution.split("x");
	framerate = document.querySelector('input[name="framerate"]:checked').value;
	mode = document.querySelector('input[name="mode"]:checked').value;
	quality = document.getElementById('quality').value;
	
	startVideo(resolutionSplit[0], resolutionSplit[1], framerate, mode, quality);
	
	setTimeout(reloadVideoIframe, 5000);
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

function startVideo(width,height,framerate,mode,quality)
{
	message = "v,";
	message += width;
	message += ",";
	message += height;
	message += ",";
	message += framerate;
	message += ",";
	message += mode;
	message += ",";
	message += quality;
	sendWebsocket(message);
	
}

function controlInterval()
{
	scangamepads();
	for (j in controllers) {
		var controller = controllers[j];
		
		var data = new Array(5);
		data[0] = team;
		
		if ( controlMode == 'absolute')
		{
			//rotary
			values[0] = controller.axes[0] * (Math.PI / 2.0000);
			//linear
			values[1] = controller.axes[1];
			//rotary
			values[2] = controller.axes[2] * (Math.PI / 2.0000);
			//linear
			values[3] = controller.axes[3];
		}
		
		if ( controlMode == 'relative')
		{
			values[0] = values[0] + (controller.axes[0].toFixed(4) * globalSensitivty);
			if( values[0] > (Math.PI / 2.0000)) values[0] = (Math.PI / 2.0000);
			if( values[0] < (Math.PI / -2.0000)) values[0] = (Math.PI / -2.0000);
			
			values[1] = values[1] + (controller.axes[1].toFixed(4) * globalSensitivty);
			if( values[1] > 1) values[1] = 1;
			if( values[1] < -1) values[1] = -1;
			
			values[2] = values[2] + (controller.axes[2].toFixed(4) * globalSensitivty);
			if( values[2] > (Math.PI / 2.0000)) values[2] = (Math.PI / 2.0000);
			if( values[2] < (Math.PI / -2.0000)) values[2] = (Math.PI / -2.0000);
			
			values[3] = values[3] + (controller.axes[3].toFixed(4) * globalSensitivty);
			if( values[3] > 1) values[3] = 1;
			if( values[3] < -1) values[3] = -1;
		}
		
		data[1] = values[3].toFixed(4);
		data[2] = values[2].toFixed(4);
		data[3] = values[1].toFixed(4);
		data[4] = values[0].toFixed(4);
 
		sendWebsocket(data);
	
	}
}

function changeControl(sensitivity, rate)
{
	globalSensitivty = sensitivity;
	values[0] = 0;
	values[1] = 0;
	values[2] = 0;
	values[3] = 0;
	clearInterval(intervalTimer);
	milliRate = 1000 / rate;
	intervalTimer = setInterval(controlInterval, milliRate);
	
}

function sendWebsocket(data)
{
	if (socket.readyState === WebSocket.OPEN) {
		socket.send(data);
	}
	
}

function webSocketConnect()
{
	//ip = document.getElementById('websocketAddress').value;
	var socketAddress = "ws://" + location.hostname + ":6789/";
	socket = new WebSocket(socketAddress);
}

function changeTeam(teamChange)
{
	team = teamChange
}

function connecthandler(e)
{
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad; var d = document.createElement("div");
}

function disconnecthandler(e)
{
  removegamepad(e.gamepad);
}

function removegamepad(gamepad)
{
  delete controllers[gamepad.index];
}

function scangamepads()
{
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i] && (gamepads[i].index in controllers)) {
      controllers[gamepads[i].index] = gamepads[i];
    }
  }
}

if (haveEvents)
{
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}
