import tkinter as tk
from tkinter import ttk

class LoggingMenu(object):
    """docstring for LoggingMenu"""
    def __init__(self, parentFrame, panelManager):
        super(LoggingMenu, self).__init__()

        self.PM = panelManager
        self.logfile = None

        self.frame = ttk.Frame(parentFrame, padding="3 3 12 12", borderwidth="2", relief="raised")
        self.frame.grid(column=0, row=0, sticky=(tk.E, tk.W), columnspan=2)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=3)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        self.title = ttk.Label(self.frame, text="Logging filename: ", style='Info.TLabel')

        self.filename = tk.StringVar()
        self.filenameEntry = ttk.Entry(self.frame, textvariable=self.filename)

        self.startButton = ttk.Button(self.frame, text="Start", command=self.startLogfile)
        self.stopButton = ttk.Button(self.frame, text="Stop", command=self.closeLogfile)
        self.stopButton.state(['disabled'])

        self.progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, mode='indeterminate')

        self.title.grid(column=0, row=0, sticky=(tk.E, tk.W), padx=5, pady=5, rowspan=2)
        self.filenameEntry.grid(column=1, row=0, sticky=(tk.E, tk.W), padx=5, pady=5, rowspan=2)
        self.startButton.grid(column=2, row=0, sticky=(tk.E, tk.W), padx=5, pady=5)
        self.stopButton.grid(column=3, row=0, sticky=(tk.E, tk.W), padx=5, pady=5)
        self.progress.grid(column=2, row=1, sticky=(tk.E, tk.W), padx=5, pady=5, columnspan=2)

    def startLogfile(self):
        if self.filename.get() is not "":
            if self.PM.sensorToLog():
                print("Log with file: " + self.filename.get() + ".log")
                self.progress.start()

                try:
                    self.logfile = open(self.filename.get() + ".log", 'a')
                except:
                    raise
                
                self.startButton.state(['disabled'])
                self.stopButton.state(['!disabled'])

                self.PM.startLogging(self.logfile)
            else:
                print("No sensor to log")
        else:
            print("Log filename invalid")

    def closeLogfile(self):
        print("Stopping log")
        self.progress.stop()

        try:
            self.logfile.close()
        except:
            raise

        self.stopButton.state(['disabled'])
        self.startButton.state(['!disabled'])

        self.PM.stopLogging()