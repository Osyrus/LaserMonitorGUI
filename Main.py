import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import Panels
import Menus

rootWindow = tk.Tk()
rootWindow.title("MQTT Laser Monitor")
rootWindow.columnconfigure(0, weight=1)
rootWindow.rowconfigure(0, weight=1)

rootWindow.option_add('*tearOff', tk.FALSE)

menuBar = tk.Menu(rootWindow)
rootWindow['menu'] = menuBar
menuFile = tk.Menu(menuBar)
menuEdit = tk.Menu(menuBar)

menuBar.add_cascade(menu=menuFile, label="File")
menuBar.add_cascade(menu=menuEdit, label="Edit")

sensorFrame = ttk.LabelFrame(rootWindow, padding="3 3 12 12", text="Sensors")
sensorFrame.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
sensorFrame.columnconfigure(0, weight=1)
sensorFrame.rowconfigure(0, weight=1)

client = mqtt.Client()
client.connect("10.32.98.69", 1883, 60)
client.loop_start();

s = ttk.Style()
s.configure('Info.TLabel', font='helvetica 16')
s.configure('Data.TLabel', font='helvetica 24')
s.configure('TCheckbutton', font='helvetica 16')
s.configure('TEntry', font='helvetica 16')

PM = Panels.PanelManager()
LM = Menus.LoggingMenu(rootWindow, PM)

sensorList = []

def processSensorList(client, userdata, message):
    payload = message.payload.decode('utf-8')

    splitMessage = payload.split(",")

    sensorList.clear()

    for sensorID in splitMessage:
        if sensorID == "sensors":
            continue

        sensorID.strip()
        sensorList.append(sensorID)

    print(sensorList)

sensorTopic = "laser/sensors/"

queryTopic = sensorTopic + "query"
sensorIdTopic = sensorTopic + "ids"

client.subscribe(sensorIdTopic)
client.message_callback_add(sensorIdTopic, processSensorList)

client.publish(queryTopic, "all", 2, retain=False)

def addSensorPanels():
    pass

D1TempTopic = "laser/sensors/temp/d1"
D1TempInfo = ("Diode 1 Thermistor", "Temperature", "C", "D1t")
D1Temp = Panels.SensorPanel(sensorFrame, D1TempInfo, D1TempTopic)

D2TempTopic = "laser/sensors/temp/d2"
D2TempInfo = ("Diode 2 Thermistor", "Temperature", "C", "D2t")
D2Temp = Panels.SensorPanel(sensorFrame, D2TempInfo, D2TempTopic)

DCurrentTopic = "laser/sensors/current/dr1"
DCurrentInfo = ("Diode Driver", "Current", "A", "DCu")
DCurrent = Panels.SensorPanel(sensorFrame, DCurrentInfo, DCurrentTopic)

PM100DTopic = "laser/sensors/power/m1"
PM100DInfo = ("PM100D Power Meter", "Power", "mW", "Pow")
PM100D = Panels.SensorPanel(sensorFrame, PM100DInfo, PM100DTopic)

PM.addSensorPanel(D1Temp, client)
PM.addSensorPanel(D2Temp, client)
PM.addSensorPanel(DCurrent, client)
PM.addSensorPanel(PM100D, client)

rootWindow.mainloop()