#!/usr/bin/python

import paho.mqtt.publish as publish 

from time import time, sleep
from os import environ

def pub():
    while(True):
        publish.single("test/test", "%s: HEARTBEAT".format(str(time())), hostname='0.0.0.0', port=int(environ['MQTT_PORT']))
        sleep(60)

if __name__ == '__main__':
    pub()
