import sockeio

sio = sockeio.Client()

sio.connect('http://localhost:3000')
@sio.on('connect')
def connect_handler():
    print('Connected!')