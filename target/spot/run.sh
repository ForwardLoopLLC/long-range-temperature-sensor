#!/bin/bash
BUS=1 # change this value to match the i2c bus where your mlx90614 is connected
mkdir -p /drivers/i2c/
mkdir -p /drivers/mlx90614/
mkdir -p /mlx90614/data/
cp /dependency/mlx90614/include/i2c/linux/*.h /drivers/i2c/
cp /dependency/mlx90614/mlx90614/*.h /drivers/mlx90614/
g++ /dependency/mlx90614/example/file_api_linux.cpp -I/drivers -o out && \
    ./out
