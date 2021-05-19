import http.server
import socketserver
import websockets
import asyncio

from threading import Thread

import abc
#import simpleServo
import testHardware

def decodeMessage(message):
    #print(message)
    arr = message.split(',')
    for word in arr:
        print(word)
    #if(arr[0] == '0'):
    #    print(arr[1])
    #    team 1
    #if(arr[0] == '1'):
        #team 2
    #message = self.data_string.decode("utf-8")
    #arr = message.split(',')

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
    start_server = websockets.serve(server, "localhost", 6789)

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
