import tkinter as tk
from tkinter import ttk

class PanelManager(object):
    """docstring for PanelManager"""
    def __init__(self):
        super(PanelManager, self).__init__()

        self.sensors = []

        self.columns = 2

        self.nextColumn = 1
        self.nextRow = 1

    def moveToNextPos(self):
        self.nextColumn += 1

        if self.nextColumn > self.columns:
            self.nextColumn = 1
            self.nextRow += 1

    def addSensorPanel(self, sensor, mqttClient):
        sensor.placeInGrid((self.nextColumn, self.nextRow))
        self.moveToNextPos()

        mqttClient.subscribe(sensor.getTopic())
        mqttClient.message_callback_add(sensor.getTopic(), sensor.mqttCallback)

        self.sensors.append(sensor)
        

class SensorPanel(object):
    """docstring for SensorPanel"""
    def __init__(self, parentFrame, sensorInfo, mqttTopic):
        super(SensorPanel, self).__init__()
        
        self.info = sensorInfo
        self.topic = mqttTopic
        self.log = tk.StringVar()
        self.log.set("0")

        self.frame = ttk.Frame(parentFrame, padding="3 3", borderwidth="2", relief="raised")

        self.title = ttk.Label(self.frame, text=self.info[0])
        self.title.grid(column=1, row=1, sticky=(tk.E, tk.W))

        self.paramDisplay = ttk.Label(self.frame, text=self.info[1])
        self.paramDisplay.grid(column=5, row=1, sticky=(tk.E, tk.W))

        self.dataStr = tk.StringVar()
        self.dataStr.set("Waiting...")
        self.dataDisplay = ttk.Label(self.frame, textvariable=self.dataStr, justify="center")
        self.dataDisplay.grid(column=1, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.logCheck = ttk.Checkbutton(self.frame, text="Log", variable=self.log)
        self.logCheck.grid(column=1, row=3, sticky=(tk.E, tk.W))

        self.topicDisplay = ttk.Label(self.frame, text=self.topic)
        self.topicDisplay.grid(column=3, row=3, sticky=(tk.E, tk.W))

    def mqttCallback(self, client, userdata, message):
        payload = message.payload.decode('utf-8')

        splitMessage = payload.split(" ")

        timestamp = splitMessage[0]
        data = float(splitMessage[1])

        self.dataStr.set("{0:02.02f} ".format(data) + self.info[2])

    def getTopic(self):
        return self.topic

    def placeInGrid(self, gridPos):
        self.frame.grid(column=gridPos[0], row=gridPos[1], sticky=(tk.N, tk.W, tk.E, tk.S))