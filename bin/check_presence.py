from context import lib
import requests
import json
from datetime import datetime
import time
import os
import configparser
from lib.jeedom import Jeedom

##### Define functions

def check_timeout(equipements,presence_timeout):
    timeout = True
    time = datetime.now()
    for equipement in equipements:
        timedelta = time - equipements[equipement]["last_positive_state"]
        if timedelta.total_seconds() < int(presence_timeout) :
            timeout = False
            break
    return timeout


#### Read Configuration

config_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','config','config.ini'))
config = configparser.ConfigParser()
config.read(config_file)

#### Main
config['JEEDOM']['HOSTNAME']
equipements = {}
jeedom = Jeedom(config['JEEDOM']['PROTOCOL'],config['JEEDOM']['HOSTNAME'],config['JEEDOM']['API_KEY'])

while True:
    datas = jeedom.get_all_data()
    for object in datas:
        if( object['name'] == config['PRESENCE']['OBJECT_DEVICES'] ):
            for equipement in object['eqLogics']:
                if( equipement['id'] not in equipements ):
                    equipements[equipement['id']] = {
                        "name" : equipement['name'],
                        "last_positive_state" : datetime.fromtimestamp(0)
                    }
                for cmd in equipement['cmds']:
                    if(cmd['logicalId'] == 'ping'):
                        if(cmd['state'] == 1):
                            equipements[equipement['id']]["last_positive_state"] = datetime.now()
    if( check_timeout(equipements,config['PRESENCE']['TIMEOUT']) ):
        jeedom.get_call(
            "/core/api/jeeApi.php?plugin=virtual&apikey={key}&type=virtual&id={cmd_id}&value={value}".format(
                key = config['PRESENCE']['VIRTUAL_DEVICE_API_KEY'],
                cmd_id = config['PRESENCE']['VIRTUAL_DEVICE_COMMAND_ID'],
                value = '0'
            )
        )
    else:
        jeedom.get_call(
            "/core/api/jeeApi.php?plugin=virtual&apikey={key}&type=virtual&id={cmd_id}&value={value}".format(
                key = config['PRESENCE']['VIRTUAL_DEVICE_API_KEY'],
                cmd_id = config['PRESENCE']['VIRTUAL_DEVICE_COMMAND_ID'],
                value = '1'
            )
        )
    time.sleep(2)