import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import Panels

rootWindow = tk.Tk()
rootWindow.title("MQTT Laser Monitor")

mainframe = ttk.Frame(rootWindow, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

client = mqtt.Client()
client.connect("10.32.98.69", 1883, 60)
client.loop_start();

PM = Panels.PanelManager()

D1TempTopic = "laser/sensors/adc/1"
D1TempInfo = ("Diode 1 Thermistor", "Temperature", "C")
D1Temp = Panels.SensorPanel(mainframe, D1TempInfo, D1TempTopic)

D2TempTopic = "laser/sensors/adc/2"
D2TempInfo = ("Diode 2 Thermistor", "Temperature", "C")
D2Temp = Panels.SensorPanel(mainframe, D2TempInfo, D2TempTopic)

DCurrentTopic = "laser/sensors/adc/3"
DCurrentInfo = ("Diode Driver", "Current", "A")
DCurrent = Panels.SensorPanel(mainframe, DCurrentInfo, DCurrentTopic)

PM100DTopic = "laser/sensors/ivi/1"
PM100DInfo = ("PM100D Power Meter", "Power", "mW")
PM100D = Panels.SensorPanel(mainframe, PM100DInfo, PM100DTopic)

PM.addSensorPanel(D1Temp, client)
PM.addSensorPanel(D2Temp, client)
PM.addSensorPanel(DCurrent, client)
PM.addSensorPanel(PM100D, client)

rootWindow.mainloop()