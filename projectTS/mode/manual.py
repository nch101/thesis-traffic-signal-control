import time

def manual(sio, quantity):
    @sio.on('news', namespace = '/data-collect')
    def changeLight(data):
        print('Received data: ', data)
        for index in range(0, quantity):
            if (lightStatus[index] == 'red'):
                lightStatus[index] = 'green'
            elif (lightStatus[index] == 'yellow'):
                lightStatus[index] = 'red'
            elif (lightStatus[index] == 'green'):
                lightStatus[index] = 'yellow'
                time.sleep(timeYellow[index])