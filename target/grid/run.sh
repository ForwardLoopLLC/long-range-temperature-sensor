#!/bin/bash
BUS=0 # change this value to match the i2c bus where your amg8833 is connected
mkdir -p /drivers/i2c/
mkdir -p /drivers/amg8833/
mkdir -p /amg8833/data/
cp /dependency/amg8833/include/i2c/linux/*.h /drivers/i2c/
cp /dependency/amg8833/amg8833/*.h /drivers/amg8833/
g++ /dependency/amg8833/example/file_api_linux.cpp -I/drivers -o out && \
    ./out
