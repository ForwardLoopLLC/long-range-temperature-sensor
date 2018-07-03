#!/bin/bash
export MQTT_SUB=./../../sub/
export MQTT_PUB=./../../pub/
export MQTT_HOST=0.0.0.0
export MQTT_PORT=1883 
docker-compose -f dependency/mqtt/docker-compose.yml build && \
docker-compose -f dependency/mqtt/docker-compose.yml up 
