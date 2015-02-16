import tkinter as tk
from tkinter import ttk

class PanelManager(object):
    """docstring for PanelManager"""
    def __init__(self):
        super(PanelManager, self).__init__()

        self.sensors = []

        self.columns = 2

        self.nextColumn = 0
        self.nextRow = 0

    def moveToNextPos(self):
        self.nextColumn += 1

        if self.nextColumn > (self.columns - 1):
            self.nextColumn = 0
            self.nextRow += 1

    def addSensorPanel(self, sensor, mqttClient):
        sensor.placeInGrid((self.nextColumn, self.nextRow))
        self.moveToNextPos()

        mqttClient.subscribe(sensor.getTopic())
        mqttClient.message_callback_add(sensor.getTopic(), sensor.mqttCallback)

        self.sensors.append(sensor)

    def startLogging(self, logfile):
        for sensor in self.sensors:
            if sensor.toLog():
                sensor.logToFile(logfile)

    def stopLogging(self):
        for sensor in self.sensors:
            sensor.stopLogging()

    def sensorToLog(self):
        for sensor in self.sensors:
            if sensor.toLog():
                return True
        return False
        

class SensorPanel(object):
    """docstring for SensorPanel"""
    def __init__(self, parentFrame, sensorInfo, mqttTopic):
        super(SensorPanel, self).__init__()
        
        self.info = sensorInfo
        self.topic = mqttTopic

        self.log = tk.StringVar()
        self.log.set("0")
        self.logging = False
        self.logfile = None
        self.logID = sensorInfo[3]

        self.frame = ttk.Frame(parentFrame, padding="3 3 12 12", borderwidth="2", relief="raised")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        self.title = ttk.Label(self.frame, text=self.info[0], style='Info.TLabel')

        self.paramDisplay = ttk.Label(self.frame, text=self.info[1], style='Info.TLabel', anchor="e")
        
        self.dataStr = tk.StringVar()
        self.dataStr.set("Waiting... ")
        self.dataDisplay = ttk.Label(self.frame, textvariable=self.dataStr, style='Data.TLabel', anchor="e")
        
        self.dataUnitDisplay = ttk.Label(self.frame, text=self.info[2], style='Data.TLabel', anchor="w")

        self.logCheck = ttk.Checkbutton(self.frame, text="Log", variable=self.log)

        self.topicDisplay = ttk.Label(self.frame, text=self.topic, style='Info.TLabel', anchor="e")

        self.title.grid(column=0, row=0, sticky=(tk.E, tk.W), columnspan=3, padx=5, pady=5)
        self.paramDisplay.grid(column=3, row=0, sticky=(tk.E, tk.W), padx=5, pady=5)
        self.dataDisplay.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), columnspan = 3, padx=5, pady=5)
        self.dataUnitDisplay.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        self.logCheck.grid(column=0, row=2, sticky=(tk.E, tk.W), padx=5, pady=5)
        self.topicDisplay.grid(column=1, row=2, sticky=(tk.E, tk.W), padx=5, pady=5)

        # ttk.Sizegrip(self.frame).grid(column=3, row=3, sticky=(tk.S, tk.E))


    def mqttCallback(self, client, userdata, message):
        payload = message.payload.decode('utf-8')

        splitMessage = payload.split(" ")

        timestamp = float(splitMessage[0])
        data = float(splitMessage[1])

        if self.logging:
            try:
                self.logfile.write(self.logID + " " + str(timestamp) + " " + str(data) + "\n")
            except:
                raise

        self.dataStr.set("{0:02.02f} ".format(data) + " ")

    def getTopic(self):
        return self.topic

    def placeInGrid(self, gridPos):
        self.frame.grid(column=gridPos[0], row=gridPos[1], sticky=(tk.N, tk.W, tk.E, tk.S))

    def toLog(self):
        if self.log.get() == "0":
            return False
        elif self.log.get() == "1":
            return True

    def logToFile(self, logfile):
        self.logging = True
        self.logfile = logfile

    def stopLogging(self):
        self.logging = False
        self.logfile = None