#!/usr/bin/python

import paho.mqtt.client as mqtt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib.dates import DateFormatter
import numpy as np

from datetime import datetime
from os import environ

import paho.mqtt.client as mqtt

_MAX_TEMP = environ.get('MLX90614_MAX_TEMP') or 50.0

class StreamingLinePlot():
    def __init__(self, fig, subplot, max_buffer=25, color='k-',
            xlabel=None, ylabel=None, xticklabels=None, yticklabels=None, title=None):
        plt.ion()
        self.max_buffer = max_buffer
        self.fig = fig
        self.ax = self.fig.add_subplot(subplot)
        self.ax.set_ylim(0.0, _MAX_TEMP)
        self.line, = self.ax.plot([], [], color, markersize=4, marker='o')
        if xlabel is not None:
            self.ax.set_xlabel(xlabel)
        if ylabel is not None:
            self.ax.set_ylabel(ylabel)
        if xticklabels is not None:
            self.ax.set_xticklabels(xticklabels)
        if yticklabels is not None:
            self.ax.set_yticklabels(yticklabels)
        if title is not None:
            self.ax.set_title(title)

    def update(self, xdata, ydata):
        current_xdata = self.line.get_xdata()
        if len(current_xdata) + len(xdata) > self.max_buffer:
            current_xdata = current_xdata[len(xdata):]
        self.line.set_xdata(np.append(current_xdata, xdata))
        current_ydata = self.line.get_ydata()
        if len(current_ydata) + len(ydata) > self.max_buffer:
            current_ydata = current_ydata[len(ydata):]
        self.line.set_ydata(np.append(current_ydata, ydata))
        self.ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.fig.autofmt_xdate()
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)
        self.fig.canvas.flush_events()

class StreamingGridPlot():
    def __init__(self, fig, subplot, title=None):
        plt.ion()
        self.fig = fig
        self.ax = self.fig.add_subplot(subplot)
        self.ax.set_xticklabels(range(0,9))
        self.ax.set_yticklabels(range(0,9))
        self.grid = self.ax.matshow(np.zeros((8,8)), cmap='hot', norm=colors.Normalize(vmin=0.0, vmax=_MAX_TEMP))
        plt.colorbar(self.grid, ax=self.ax, orientation='vertical')
        if title is not None:
            self.ax.set_title(title, y=1.15)

    def update(self, grid_data):
        self.grid.set_data(grid_data)
        self.fig.canvas.flush_events()

class MQTTClient(mqtt.Client):
    def __init__(self):
        super().__init__()
        self.fig = plt.figure()
        self.gs = gs.GridSpec(nrows=3, ncols=2)
        self.grid_temperature_plot = StreamingGridPlot(self.fig, self.gs[:2, 0], title='Object (Grid)')
        self.thermistor_temperature_line_plot = StreamingLinePlot(self.fig, self.gs[2, 0], xlabel='Time', ylabel='Temperature (°C)', title='Thermistor') 
        self.object_temperature_line_plot = StreamingLinePlot(self.fig, self.gs[:2, 1], xticklabels=[], ylabel='Temperature (°C)', title='Object (Spot)')
        self.ambient_temperature_line_plot = StreamingLinePlot(self.fig, self.gs[2, 1], xlabel='Time', ylabel='Temperature (°C)', title='Ambient')
        plt.show(block=False)

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        try:
            if msg.topic == 'test/test':
                print(msg)
            if msg.topic == 'data/spot':
                timestamp, object_temperature, ambient_temperature = msg.payload.decode('utf-8').split(',')
                time = datetime.fromtimestamp(float(timestamp))
                self.object_temperature_line_plot.update([time], [float(object_temperature)])
                self.ambient_temperature_line_plot.update([time], [float(ambient_temperature)])
            elif msg.topic == 'data/grid':
                timestamp, thermistor_temperature, grid_temperature = msg.payload.decode('utf-8').split(',')
                time = datetime.fromtimestamp(float(timestamp))
                grid_data = [[float(val) for val in row.split(' ') if val != '']
                        for row in grid_temperature.split('\n')[1:] if row != '']
                self.grid_temperature_plot.update(grid_data)
                self.thermistor_temperature_line_plot.update([time], [float(thermistor_temperature)])
        except Exception as e:
            print("ERROR: " + repr(e))
            print(msg.payload.decode('utf-8'))
            pass

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        rc = 0
        while(True):
            self.connect("0.0.0.0", 1883, 60)
            self.subscribe("test/test", 0)
            self.subscribe("data/grid", 0)
            self.subscribe("data/spot", 0)

            rc = 0
            while rc == 0:
                rc = self.loop()
        return rc

if __name__ == '__main__':
    mqtt_client = MQTTClient()
    mqtt_client.run()
