# ** automatic control mode **
# * Author: Nguyen Cong Huy
# ****************************
from dotenv import load_dotenv
import os
import 'get.socket'

load_dotenv()

getdataURL = os.getenv('GET_DATA_URL')
trafficLightID1 = os.getenv('TRAFFIC_LIGHT1_ID')
trafficLightID2 = os.getenv('TRAFFIC_LIGHT2_ID')
trafficLightID3 = os.getenv('TRAFFIC_LIGHT3_ID')
trafficLightID4 = os.getenv('TRAFFIC_LIGHT4_ID')

sio.emit('current-time', data=CurrentTime, namespace='/current-time/'+trafficLightID1)

def init(getdataURL, trafficLightID1, trafficLightID2):
    pass

def automatic():

sio.on('change-mode', namespace='/')


