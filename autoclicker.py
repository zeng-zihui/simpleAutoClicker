import tkinter as tk
import customtkinter as ctk
import ctypes
import time
import threading

class AutoClicker(ctk.CTk):
    def __init__(self):

        #Setting up the interface
        super().__init__()
        self.title("Simple Autoclicker")
        self.geometry("200x300")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        self.rowPos = 0

        self.timeVars = {
            "hour": tk.IntVar(value = 0),
            "minute": tk.IntVar(value = 0),
            "second": tk.IntVar(value = 0),
            "millisecond": tk.IntVar(value = 100)
        }
        self.hotkey = "F6" #Default hotkey
        self.is_running = False

        self.createTimeInput()
        self.createButtons()
        #self.createHotKeyInput()
        
    def createTimeInput(self):
        columnPos = 0
        for name, var in self.timeVars.items():
            xAxisPadding = (20, 0) if name == "hour" or name == "second" else (0, 20)
            tk.Label(self, text = name.capitalize()).grid(row = self.rowPos, column = columnPos, padx = xAxisPadding)
            tk.Entry(self, textvariable = var, width = 10).grid(row = self.rowPos + 1, column = columnPos, padx = xAxisPadding)
            print(name, self.rowPos)
            if name == "minute" or name == "millisecond":
                self.rowPos += 2
            columnPos = (columnPos + 1) % 2
    
    def createButtons(self):
        self.startBtn = ctk.CTkButton(self, text = "Start", command = self.start, width = 75)
        self.startBtn.grid(row = self.rowPos, column = 0, padx = (20, 0), pady = (20, 20))

        self.stopBtn = ctk.CTkButton(self, text = "Stop", command = self.stop, state = "disabled", width = 75)
        self.stopBtn.grid(row = self.rowPos, column = 1, padx = (0, 20), pady = (20, 20))

        self.rowPos += 1

    def start(self):
        self.is_running = True
        self.startBtn.configure(state = "disabled")
        self.stopBtn.configure(state = "normal")
        threading.Thread(target=self.clicker, daemon = True).start()


    def clicker(self):
        self.is_running = True
        delay = self.getDelaySeconds()
        while self.is_running:
            self.click()
            time.sleep(delay)

    def stop(self):
        self.is_running = False
        self.startBtn.configure(state = "normal")
        self.stopBtn.configure(state = "disabled")

    def getDelaySeconds(self):
        hour = self.timeVars["hours".get()]
        minute = self.timeVars["minute"].get()
        second = self.timeVars["second"].get()
        millisecond = 10 if self.timeVars["millisecond"].get() <= 10 else self.timeVars["millisecond"].get()
        return (hour * 3600) + (minute * 60) + second + (millisecond / 1000)
    
    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)


if __name__ == "__main__":
    app = AutoClicker()
    app.mainloop()