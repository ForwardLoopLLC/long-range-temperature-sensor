========================
Custom Application Guide
========================

Overview
========
This guide covers how to modify the demonstration application to use your own target and host application code. You can read live temperature data from almost any application you want on your Forward Loop Zero and then digest that data over MQTT using almost any application on your host.

The guide assumes you are familiar with the instructions in the :doc:`demo`.

Throughout this guide, all code changes are based on the demonstration application code, which can be found in the `Demonstration Application GitHub repository <https://github.com/ForwardLoopLLC/long-range-temperature-sensor>`_.

Modify the Target Application
=============================
You can find all of the target application code in the **long-range-temperature-sensor/target** folder.

Overview
--------
The target application runs on your Forward Loop Zero in Docker and performs the following steps:
    - follows the instructions in **Dockerfile.linux** and installs Docker Compose inside of the Docker container
    - runs the script **run.sh** to start the services defined in **docker-compose.yml**, which are:
        - a *network* service that reads files **/data/mlx90614/data** and **/data/amg8833/data** inside of the container then publishes the data read from those files to the MQTT topics *data/spot* and *data/grid*, respectively
        - a *spot* service that reads temperature data from the MLX90614 sensor and continuously updates **/data/mlx90614/data** with that data in the *network* container
        - a *grid* service that reads temperature data from the AMG8833 sensor and continuously updates **/data/amg8833/data** with that data in the *network* container

Network Folder
--------------
In order to read live data from both sensors, process that data, and pass that processed data over MQTT, you should only need to change the files in the **long-range-temperature-sensor/target/network** folder. You can use the same *spot* and *grid* services to read live data inside of the *network* service container.

Specifically, the **network** folder **must** contain at least two files:
    - **Dockerfile**: a Dockerfile that specifies the build environment and dependencies for your data processing *network* service. Strictly speaking, your *network* service does **not** need to pass data over a network, though this is the easiest way to respond to data read from your Forward Loop Zero.
    - **run.sh**: a shell script that runs the *network* service application code for your custom target application. All source files in the **network** folder are accessible inside of the *network* service container inside of the folder **/network/**. Note that the last line of this script should typically run in an infinite loop, otherwise the service will stop when the script finishes.

While you could write your entire custom target application inside of **run.sh**, you can also specify other files inside of the **network** folder in order to define more complicated custom target applications. For example, the demonstration application **run.sh** calls Python to run a script that reads data from the sensors and publishes that data to an MQTT broker. 

Sensor File APIs
----------------
No matter what custom target application Docker environment you choose, you can access the live temperature data from both sensors through two simple file interfaces inside of the *network* service container:
    - **/data/mlx90614/data**: a list of comma-separated values read from the MLX90614 long-range infrared sensor. The *spot* service updates the temperature with a delay between measurements specified in the *MLX90614_DELAY* environment variable under the *mlx90614* service in the **docker-compose.yml** file in the **network** folder. Note that they delay value is specified in milliseconds. The values in the data file are organized as follows:
    .. code-block:: bash

        # Note the \n newline at the end
        Unix epoch timestamp in seconds (with milliseconds as decimals),
        object temperature in Celsius,
        ambient temperature in Celsius \n

    You can see the :download:`C++ source definition <../../../target/dependency/mlx90614/example/file_api_linux.cpp>` of the *spot* service for more information.

    - **/data/amg883/data**: a list of comma-separated and newline-separated values read from the AMG8833 grid-eye infrared sensor. The *grid* service updates the temperature grid with a delay of 0.1 seconds between measurements. The values in the data file are organized as follows:
    .. code-block:: bash

        # Note the \n newline between theristor and grid
        Unix epoch timestamp in seconds (with milliseconds as decimals),
        thermistor temperature in Celsius, \n
        grid temperatures organized as
        eight newline-separated (\n) rows of
        eight space-separated (\s) temperatures in Celsius

    You can see the :download:`C++ source definition <../../../target/dependency/amg8833/example/file_api_linux.cpp>` of the *grid* service for more information.
Using these file APIs, your custom target application can read temperature values from a file, process that data, and then pass it over a network as needed. Note that the target application *spot* and *grid* services do not prevent race conditions and data corruption due to simultaneous read and writes, so you application code should be designed to handled nonexistent and corrupted data files. Typically, these errors will not happen if you read the files at a frequency lower than that specified by the delay between the data file writes, though there are no guarantees that this is the case.

Run the Application
-------------------
Once you have defined the custom target application source code in the **network** folder, you can run the target application by following the same steps in the :doc:`demo`.

Modify the Host Application
===========================
You can find the host application code in the **long-range-temperature-sensor** folder.

Overview
--------
The host application runs on your local machine with Docker and Docker Compose and performs the following steps:
    - runs Docker Compose with the configuration file defined in **long-range-temperature-sensor/dependency/mqtt/docker-compose.yml**, which defines the following services:
        - a *broker* service that defines a standard MQTT broker that runs on the *MQTT_HOST* at the *MQTT_PORT* defined in the **long-range-temperature-sensor/plot.sh** script
        - a *pub* service that publishes data to the MQTT broker, with source code defined in **long-range-temperature-sensor/pub**
        - a *sub* service that subscribes to the MQTT broker, with source code defined in **long-range-temperature-sensor/sub**

For more information on the MQTT drivers, see the `MQTT Driver Documentation <https://docs.forward-loop.com/drivers/mqtt/master/index.html>`_.

Publish Service
---------------
The *pub* service is defined in the **long-range-temperature-sensor/pub** folder. 

The **pub** folder **must** contain at least one file:
    - **Dockerfile**: a Dockerfile that specifies the build environment and dependencies for an application that publishes data to MQTT topics on the broker in the *broker* service. All source files in the **pub** folder are accessible inside of the *pub* service container inside of the folder **/pub/**. 

While you could write your entire custom *pub* service inside of the **Dockerfile**, you can also specify other files that define an application that publishes data. For example, the demonstration application *pub* service calls a Python script that publishes the Unix epoch time as a heartbeat to the MQTT broker every 60 seconds on the *test/test* topic.

Subscribe Service
-----------------
The *sub* service is defined in the **long-range-temperature-sensor/sub** folder. 

The **sub** folder **must** contain at least one file:
    - **Dockerfile**: a Dockerfile that specifies the build environment and dependencies for an application that subsribes to  MQTT topics on the broker in the *broker* service. All source files in the **sub** folder are accessible inside of the *sub* service container inside of the folder **/sub/**. 

While you could write your entire custom *sub* service inside of the **Dockerfile**, you can also specify other files that define an application that subscribes to data topics. For example, the demonstration application *sub* service subscribes to heartbeat topic on *test/test* and the temperature data topics on *data/spot* and *data/grid*.

Run the Application
-------------------
Once you have defined the *pub* and *sub* services' source code in the **pub** and **sub** folders, along with the *MQTT_HOST* and *MQTT_PORT* values in **plot.sh**, you can run the host application by following the same steps in the :doc:`demo`.

Further Information
===================
The Forward Loop Zero long-range temperature sensor uses open-source, MIT-licensed code from the Forward Loop Zero ecosystem, including:

`MQTT Drivers <https://docs.forward-loop.com/drivers/mqtt/master/index.html>`_

`MLX90614 Drivers <https://docs.forward-loop.com/drivers/mlx90614/master/index.html>`_

`AMG8833 Drivers <https://docs.forward-loop.com/drivers/amg8833/master/index.html>`_

`I2C Drivers <https://docs.forward-loop.com/drivers/i2c/master/index.html>`_
