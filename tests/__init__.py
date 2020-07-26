import sys, os, urllib3
import configparser
import logging
import logging.config


projectPath = os.path.expanduser('~/Documents/py-project')
sys.path.append(projectPath)
logging.config.fileConfig(projectPath + '/projectTS/logging.conf', 
                    defaults={'logfilename': projectPath + '/projectTS/logs/app.log', 
                            'logwarnname': projectPath + '/projectTS/logs/warn.log'})


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)