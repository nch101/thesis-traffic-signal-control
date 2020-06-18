import logging
import configparser

from projectTS.lib.postData import postData
import projectTS.vals as vals

logger = logging.getLogger('projectTS.imagesProcessing.updateTrafficDensity')

config = configparser.ConfigParser()
config.read('config.ini')

default = config['DEFAULT']
postDataURL = default['postData']
interID = default['intersection_id']
token = default['access_token']

intersection = postData(postDataURL, interID, token)

def updateTrafficDensity():
    if (vals.uNS >= vals.uWS):
        intersection.postData({ 
            rate: vals.rateNS,
            state: vals.stateNS
            })
    else:
        intersection.postData({
            rate: vals.rateWS,
            state: vals.stateWS
        })