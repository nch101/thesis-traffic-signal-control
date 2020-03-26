from dotenv import load_dotenv
import os
import socketio
import time

load_dotenv()

serverAddress = os.getenv('SERVER_ADDRESS')
clientID = os.getenv('clientID')

sio = socketio.Client()
sion = socketio.ClientNamespace()

@sio.event
def connect():
    print('connection established')

@sio.on('news', namespace = '/data-collect')
def my_event(data):
    print('Received data: ', data)
    for i in range (0, 30):
        sio.emit('news', i, '/data-collect')
        time.sleep(3)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect(serverAddress)
sio.wait()  