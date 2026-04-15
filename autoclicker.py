import tkinter as tk
import customtkinter as ctk
import pyautogui
import keyboard
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
        self.hotkey = "f6" #Default hotkey
        self.hotkeyHook = None
        self.is_running = False

        self.createTimeInput()
        self.createButtons()
        self.createHotkeyInput()
    

    #Create entry and text to allow user input on click delay
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
    
    #Create button to allow user to start and stop the auto clicker
    def createButtons(self):
        self.startBtn = ctk.CTkButton(self, text = "Start", command = self.toggle, width = 75)
        self.startBtn.grid(row = self.rowPos, column = 0, padx = (20, 0), pady = (20, 20))

        self.stopBtn = ctk.CTkButton(self, text = "Stop", command = self.toggle, state = "disabled", width = 75)
        self.stopBtn.grid(row = self.rowPos, column = 1, padx = (0, 20), pady = (20, 20))

        self.rowPos += 1

    #Toggles the auto clicker
    def toggle(self):
        if not self.is_running:
            self.is_running = True
            self.startBtn.configure(state = "disabled")
            self.stopBtn.configure(state = "normal")
            threading.Thread(target=self.clicker, daemon = True).start()
        else:
            self.is_running = False
            self.startBtn.configure(state = "normal")
            self.stopBtn.configure(state = "disabled")

    #Calculates the delay of each click
    def getDelaySeconds(self):
        hour = self.timeVars["hour"].get()
        minute = self.timeVars["minute"].get()
        second = self.timeVars["second"].get()
        millisecond = self.timeVars["millisecond"].get()
        return (hour * 3600) + (minute * 60) + second + (millisecond / 1000)
    
    #The function that performs the click
    def clicker(self):
        delay = self.getDelaySeconds()
        while self.is_running:
            ctypes.windll.user32.mouse_event(2,0,0,0,0)
            ctypes.windll.user32.mouse_event(4,0,0,0,0)
            time.sleep(delay)

    #The button and text to allow user change hotkey input
    def createHotkeyInput(self):
        ctk.CTkLabel(self, text="Hotkey").grid(row=self.rowPos, column=0, columnspan=2, pady=(5, 0))
        self.rowPos += 1
        self.hotkeyBtn = ctk.CTkButton(self, text=f"Current: {self.hotkey}", command=self.listenForHotkey)
        self.hotkeyBtn.grid(row=self.rowPos, column=0, columnspan=2, pady=5)
        self.rowPos += 1
        self.bindHotkeys()

    #Allows user to change hotkey
    def listenForHotkey(self):
        self.hotkeyBtn.configure(text="Press any key...")
        keyboard.hook(self.captureHotkey)

    #Captures what user wants as hotkey
    def captureHotkey(self, event):
        if event.event_type != "down":
            return
        if event.name in ("shift", "ctrl", "alt", "left shift", "right shift", "left ctrl", "right ctrl", "left alt", "right alt"):
            return
        
        mods = []
        if keyboard.is_pressed("ctrl"):
            mods.append("ctrl")
        if keyboard.is_pressed("shift"):
            mods.append("shift")
        if keyboard.is_pressed("alt"):
            mods.append("alt")

        mods.append(event.name)
        self.hotkey = "+".join(mods)
 
        self.hotkeyBtn.configure(text=f"Current: {self.hotkey}")
        threading.Thread(target=self.rebindHotkey, daemon = True).start()

    #Uses another thread to rebind the hotkey
    def rebindHotkey(self):
        keyboard.unhook_all()
        self.bindHotkeys()

    #Binds hotkey to the toggle function
    def bindHotkeys(self):
        if self.hotkeyHook:
            try:
                keyboard.remove_hotkey(self.hotkeyHook)
            except:
                pass
        self.hotkeyHook = keyboard.add_hotkey(self.hotkey, self.toggle)


if __name__ == "__main__":
    app = AutoClicker()
    app.mainloop()