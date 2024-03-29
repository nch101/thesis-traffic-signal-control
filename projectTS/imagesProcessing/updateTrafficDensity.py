import logging
import configparser

from projectTS.lib.postData import postData
import projectTS.vals as vals

logger = logging.getLogger('projectTS.imagesProcessing.updateTrafficDensity')

config = configparser.ConfigParser()
config.read('config.ini')

default = config['DEFAULT']
server = default['server']
postDataNsp = default['postDataNsp']
interID = default['intersection_id']
token = default['access_token']

intersection = postData(server + postDataNsp, interID, token)

def updateTrafficDensity():
    if (vals.stateWS != '' and vals.stateNS != ''):
        if (vals.rateNS >= vals.rateWS):
            result = intersection.postData({ 
                'rate': vals.rateNS,
                'state': vals.stateNS
            })
        else:
            result = intersection.postData({ 
                'rate': vals.rateWS,
                'state': vals.stateWS
            })
            
        if result:
            logger.info('Update data success')
        else:
            logger.error('Update data failed')