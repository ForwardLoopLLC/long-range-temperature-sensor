Custom Application Guide
========================

Overview
--------
This guide covers how to modify the demonstration application to use your own target and host application code. You can read live temperature data from almost any application you want on your Forward Loop Zero and then digest that data over MQTT using almost any application on your host.

The guide assumes you are familiar with the instructions in the :doc:`demo`.

Throughout this guide, all code changes are based on the demonstration application code, which can be found in the `Demonstration Application GitHub repository <https://github.com/ForwardLoopLLC/long-range-temperature-sensor>`_.

Modify the Target Application
-----------------------------
You can find all of the target application code in the **long-range-temperature-sensor/target** folder.

The target application runs in Docker and performs the following steps:
    - follows the instructions in **Dockerfile.linux** and installs Docker Compose inside of Docker
    - runs the script **run.sh** to start the services defined in **docker-compose.yml**, which are:
        - a *network* service that reads files **/data/mlx90614/data** and **/data/amg8833/data** inside of the container then publishes the data read from those files to the MQTT topics *data/spot* and *data/grid*, respectively
        - a *spot* service that reads temperature data from the MLX90614 sensor and continuously updates **/data/mlx90614/data** with that data in the *network* container
        - a *grid* service that reads temperature data from the AMG8833 sensor and continuously updates **/data/amg8833/data** with that data in the *network* container

In order to read live data from both sensors, process that data, and pass that processed data over MQTT, you should only need to change the files in the **long-range-temperature-sensor/target/network** folder. You can use the same *spot* and *grid* services to read live data inside of the *network* service container.

Specifically, the **network** folder **must** contain at least two files:
    - **Dockerfile**: a Dockerfile that specifies the build environment and dependencies for your data processing *network* service. Strictly speaking, your *network* service does **not** need to pass data over a network, though this is the easiest way to respond to data read from your Forward Loop Zero.
    - **run.sh**: a shell script that runs the *network* service application code for your custom target application. All source files in the **network** folder are accessible inside of the *network* service container inside of the folder **/network/**. Note that the last line of this script should typically run in an infinite loop, otherwise the service will stop when the script finishes.

While you could write your entire custom target application inside of **run.sh**, you can also specify other files inside of the **network** folder in order to define more complicated custom target applications. For example, the demonstration application **run.sh** calls Python to run a script that reads data from the sensors and publishes that data to an MQTT broker. 

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
