#!/usr/bin/python

import paho.mqtt.publish as publish

from multiprocessing import Process
from time import sleep

from os import environ

_HOSTNAME = environ['MQTT_HOST'] 
_PORT = int(environ['MQTT_PORT'])

def publish_data(data_file, topic, hostname, port, frequency):
    while True:
        try:
            with open(data_file, 'r') as df:
                data = df.read()
            publish.single(
                    topic,
                    data,
                    hostname=hostname,
                    port=port)
            sleep(1.0/frequency)
        except Exception as e:
            pass

def main():
    mlx90614 = Process(
            target=publish_data,
            args=('/data/mlx90614/data', 'data/spot', _HOSTNAME, _PORT, 0.5))
    mlx90614.start()
    amg8833 = Process(
            target=publish_data,
            args=('/data/amg8833/data', 'data/grid', _HOSTNAME, _PORT, 1.0))
    amg8833.start()
    mlx90614.join()
    amg8833.join()

if __name__ == '__main__':
    main()
