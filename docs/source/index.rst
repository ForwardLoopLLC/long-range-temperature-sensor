.. long-range-infrared-sensor documentation master file, created by
   sphinx-quickstart on Fri Jun 29 17:33:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Long-range Temperature Sensor
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

When you absolutely have to know how hot (or cold) it is over there!

.. image::  https://img.youtube.com/vi/zRzgaaJVDJM/0.jpg
    :target: https://www.youtube.com/watch?v=zRzgaaJVDJM

How It Works
------------
This sensor uses `Forward Loop Zero <https://forward-loop.com/product.html>`_.

The long-range temperature sensor measures temperatures up to two meters away.

The sensor uses two kinds of infrared camera: one camera precisely measures the temperature of a small spot while the other camera measures the temperatures of 64 points in an 8-by-8 grid thermal image.

The sensor reads the data and publishes it using MQTT via a broker running on your local machine. Your local machine subscribes to the data topic and presents that data as live plots of the thermal image and spot temperatures.

Buy
---
You can buy this sensor and many more as part of `Forward Loop Zero <https://forward-loop.com/product.html>`_.

Forward Loop Zero provides high quality pre-assembled and tested hardware and open-source, MIT-licensed software and networking support to help developers make the next generation of sensor and IoT applications.

Use
---
When you purchase Forward Loop Zero with the optional grid-eye and long-range sensors, your Forward Loop Zero arrives assembled and configured to run the demonstration application out of the box.

For more information about the demonstration application, please see `intro/demo`.

Build
-----
You can use the long-range temperature sensor to build your own applications that incorporate your own requirements or business logic.

For more information about the long-range temperature sensor and how to modify the demonstration application, please see the `intro/tech`.
