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
import testHardware

process = subprocess.Popen

def decodeMessage(message):
    #print(message)
    arr = message.split(',')
    for word in arr:
        print(word)
    #if(arr[0] == '0'):
    #    print(arr[1])

    #if(arr[0] == '1'):
    #    print(arr[1])

    if(arr[0] == 'v'):
        startVideo(arr[1],arr[2],arr[3],arr[4],arr[5])
        
    if(arr[0] == 's'):
        startVideo(arr[1],arr[2],arr[3],arr[4],arr[5])

def stopVideo():
    #process.terminate()
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def startVideo(width,height, framerate, mode, quality):
    #print('./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x {} -y {} -fps {} -quality {} -ex {}"'.format(width, height,framerate, mode, quality))
    #cmd = 'explorer "https://google.com"'
    #os.system(cmd)
    cmd = ('./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x {} -y {} -fps {} -quality {} -ex {}"'.format(width, height,framerate, mode, quality))
    #process = subprocess.Popen(cmd, shell=True)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
    print(cmd)

def webServer():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        print("pre test print" )
        httpd.serve_forever()
        print("test print" )
        
async def server(websocket, path):
    async for message in websocket:
        decodeMessage(message)

      #  await websocket.send(message)
    

def webSocketServer():
    

    # Create websocket server
    start_server = websockets.serve(server, "192.168.1.136", 6789)

    # Start and run websocket server forever
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

t1 = Thread(target=webServer)
#t2 = Thread(target=webSocketServer)
#t2 = Thread(target=task)

t1.start()
#t2.start()
webSocketServer()
#webServer();
#print("test print" )
#while(1):
#    print("test print" )
