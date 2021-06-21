import http.server
import socketserver
import websockets
import asyncio

import os
import signal
import subprocess

from threading import Thread

import abc
#import simpleServo
#import testHardware
import simpleServo


class webSockets():
    def __init__(self, decode):
        self.decode =  decode
        
    async def server(self,websocket, path):
        async for message in websocket:
            #print("message received" )
            self.decode.decodeMessage(message)
            
    def startWebSocketServer(self):
        print("websocket server started" )
        start_server = websockets.serve(self.server, "192.168.1.106", 6789)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    

class webServer:
    def startWebServer(self):
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            print("pre test print" )
            httpd.serve_forever()
            print("test print" )
            
    def startWebServerThread(self):
        print("serving at port")
        t1 = Thread(target=self.startWebServer)
        t1.start()
        print("thread started")
        
    
class videoControl:
    def stopVideo(self):
        cmd = ('killall mjpg_streamer')
        process = subprocess.Popen(cmd, shell=True) 
    
    def startVideo(self,width,height, framerate, mode, quality):

        cmd = ('cd streamer && ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x {} -y {} -fps {} -ex {} -quality {}"'.format(width, height,framerate, mode, quality))
    
        process = subprocess.Popen(cmd, shell=True) 
        print(cmd)


class clientServerProtocol:
    def __init__(self, video, usedHardware):
        self.videoControl =  video
        self.hardwareControl = usedHardware
        
    def decodeMessage(self, message):
        
        arr = message.split(',')
        #print("message received2" )
        if(arr[0] == '0'):
            #print(arr[0])
            self.hardwareControl.moveMotor(0,arr[1])
            self.hardwareControl.moveMotor(1,arr[2])
            self.hardwareControl.moveMotor(4,arr[3])
            self.hardwareControl.moveMotor(5,arr[4])

        if(arr[0] == '1'):
            #print(arr[1])
            self.hardwareControl.moveMotor(2,arr[1])
            self.hardwareControl.moveMotor(3,arr[2])
            self.hardwareControl.moveMotor(6,arr[3])
            self.hardwareControl.moveMotor(7,arr[4])

        if(arr[0] == 'v'):
            self.videoControl.startVideo(arr[1],arr[2],arr[3],arr[4],arr[5])
        
        if(arr[0] == 's'):
            self.videoControl.stopVideo()



webServer = webServer()  

videoControl = videoControl()
#usedHardware = testHardware.testHardware()
usedHardware = simpleServo.simpleServo()

clientServerProtocol = clientServerProtocol(videoControl, usedHardware)

webSockets = webSockets(clientServerProtocol)


        
webServer.startWebServerThread()

print("web server started" )
webSockets.startWebSocketServer()



