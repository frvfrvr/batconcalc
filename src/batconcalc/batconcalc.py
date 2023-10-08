import datetime as dt
import time
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfile
from helpers import AFKdetector, BatteryState, TimeLog

class MainWindow:
    def __init__(self, master):
        # variable setup
        self.AFKdetector = AFKdetector()
        self.afk_set_time = self.AFKdetector.afk_time
        self.timelog = TimeLog()
        self.battery = BatteryState()
        
        # GUI setup
        self.master = master
        self.master.title("Average Battery Consumption")
        self.master.resizable(0,0)
        self.master.attributes('-topmost',True)
        
        self.master.geometry('475x250')
        self.label = tk.Label(self.master, text="")
        self.label.pack()
        
        self.battery_log_table = []
        self.battery_log_var = tk.StringVar(value=self.battery_log_table)
        self.l = tk.Listbox(self.master, listvariable=self.battery_log_var, height=5, width=50)
        self.l.pack()
        
        self.notebook = ttk.Notebook(self.master)
        self.AFK_tab = ttk.Frame(self.notebook)
        
        self.AFKtime_frame = tk.LabelFrame(self.AFK_tab, text='AFK time')
        self.AFKtime_label = tk.Label(self.AFKtime_frame, text="0")
        self.AFKtime_frame.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)
        self.AFKtime_label.pack()
        
        self.AFKsecs = tk.IntVar(value=self.afk_set_time)
        self.AFKsecs_box = tk.Spinbox(self.AFKtime_frame, from_=10.0, to=9999.0, textvariable=self.AFKsecs, width=5)
        self.AFKsecs_box.pack(padx=5)
        
        self.afk_set_time = int(self.AFKsecs_box.get())
        
        self.isAFK_frame = tk.LabelFrame(self.AFK_tab, text='is AFK?')
        self.isAFK_label = tk.Label(self.isAFK_frame, text="None")
        self.isAFK_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.isAFK_label.pack(fill=tk.BOTH, expand=1)
        
        self.File_tab = ttk.Frame(self.notebook)
        
        self.savefile_button = tk.Button(self.File_tab, text="Export to new CSV file", command=self.savefile)
        self.savefile_button.pack(expand=1, fill=tk.BOTH)
        
        self.openfile_button = tk.Button(self.File_tab, text="Export to existing CSV file", command=self.openfile)
        self.openfile_button.pack(expand=1, fill=tk.BOTH)
        
        self.statusbar = tk.Label(self.File_tab, justify='center', font=(None, 10), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        
        self.notebook.add(self.AFK_tab, text='AFK setting')
        self.notebook.add(self.File_tab, text='Export to File')
        
        self.notebook.pack(expand=1, fill=tk.BOTH)
        
        self.AFKdetector.start()

    def savefile(self):
        self.file = asksaveasfile(defaultextension=".csv")
        self.battery.update()
        try:   
            self.timelog_file = self.file.name if hasattr(self, "file") else None
            self.statusbar.config(text=f"File saved to {self.timelog_file}")
            self.timelog.csv_create(self.file.name)
            self.timelog.update(timestamp=int(time.time()), battery_percent=self.battery.percent, is_charging=self.battery.is_charging, is_afk=self.AFKdetector.check_if_afk(), battery_cycle=self.battery.cycle_count)
            self.savefile_button["text"] = "Open CSV"
            self.savefile_button["command"] = lambda: self.timelog.csv_open()
            self.openfile_button["state"] = "disabled"
        except AttributeError:
            pass
        
    def openfile(self):
        self.file = askopenfile(defaultextension=".csv")
        self.battery.update()
        try:
            self.timelog_file = self.file.name if hasattr(self, "file") else None
            self.statusbar.config(text=f"File saved to {self.timelog_file}")
            strbool = lambda x: True if str(x).lower() == "true" else False
            self.battery_log_table = []
            for i in self.timelog.read_last_N_rows(5, self.file.name):
                log_timestamp = dt.datetime.fromtimestamp(int(i["timestamp"]))
                log_percent = i["battery_percent"]
                log_is_charging = "charging" if strbool(i["is_charging"]) else "not charging"
                log_is_afk = "(AFK)" if strbool(i["is_afk"]) else ''
                log_cycle = str(i["battery_cycle"]) + " cycles"
                self.battery_log_table.append(f"{log_timestamp} - {log_percent}% | {log_is_charging} {log_is_afk} ({log_cycle})")
            for i in range(len(self.timelog.data), -1, -1):
                if i == 5 or IndexError:
                    break
                self.battery_log_table.pop(0)
                log_timestamp = dt.datetime.fromtimestamp(int(self.timelog.data[-i]["timestamp"]))
                log_percent = self.timelog.data[-i]["battery_percent"]
                log_is_charging = "charging" if strbool(self.timelog.data[-i]["is_charging"]) else "not charging"
                log_is_afk = "(AFK)" if strbool(self.timelog.data[-i]["is_afk"]) else ''
                log_cycle = str(self.timelog.data[-i]["battery_cycle"]) + " cycles"
                self.battery_log_table.append(f"{log_timestamp} - {log_percent}% | {log_is_charging} {log_is_afk} ({log_cycle})")
            
            self.battery_log_var.set(self.battery_log_table)
            self.l.pack()
            self.timelog.csv_create(self.file.name)
            self.timelog.update(timestamp=int(time.time()), battery_percent=self.battery.percent, is_charging=self.battery.is_charging, is_afk=self.AFKdetector.check_if_afk(), battery_cycle=self.battery.cycle_count)
            start_time = dt.datetime.fromtimestamp(int(self.timelog.scan_last_N_rows(0, self.timelog_file)[-2]["timestamp"]))
            end_time = dt.datetime.fromtimestamp(int(self.timelog.scan_last_N_rows(0, self.timelog_file)[-1]["timestamp"]))
            time_difference = self.timelog.time_diff(start_time, end_time)
            self.label.configure(text=f"Battery {'charging' if self.battery.is_charging else 'consumes'} every {time_difference}")
            self.openfile_button["text"] = "Open CSV"
            self.openfile_button["command"] = lambda: self.timelog.csv_open()
            self.savefile_button["state"] = "disabled"
        except AttributeError:
            pass
        
    def reloop(self):
        # purpose of reloop is to update the GUI every second
        # this is done by calling the function again after 1000ms
        strbool = lambda x: True if str(x).lower() == "true" else False
        self.battery.update()
        if len(self.timelog.data) < 1:
            self.timelog.update(timestamp=int(time.time()), battery_percent=self.battery.percent, is_charging=self.battery.is_charging, is_afk=self.AFKdetector.check_if_afk(), battery_cycle=self.battery.cycle_count)
            
            log_timestamp = dt.datetime.fromtimestamp(int(self.timelog.read_last_row()["timestamp"]))
            log_percent = self.timelog.read_last_row()["battery_percent"]
            log_is_charging = "charging" if self.timelog.read_last_row()["is_charging"] else "not charging"
            log_is_afk = "(AFK)" if self.timelog.read_last_row()["is_afk"] else ''
            log_cycle = str(self.timelog.read_last_row()["battery_cycle"]) + " cycles"
            
            self.battery_log_table.append(f"{log_timestamp} - {log_percent}% | {log_is_charging} {log_is_afk} ({log_cycle})")
            self.battery_log_var.set(self.battery_log_table)
            self.l.pack()
        if len(self.timelog.data) > 0:
            if not self.timelog.check_last_row(battery_percent=self.battery.percent, is_charging=self.battery.is_charging, is_afk=self.AFKdetector.check_if_afk()):
                self.timelog.update(timestamp=int(time.time()), battery_percent=self.battery.percent, is_charging=self.battery.is_charging, is_afk=self.AFKdetector.check_if_afk(), battery_cycle=self.battery.cycle_count)
                
                log_timestamp = dt.datetime.fromtimestamp(int(self.timelog.read_last_row()["timestamp"]))
                log_percent = self.timelog.read_last_row()["battery_percent"]
                log_is_charging = "charging" if strbool(self.timelog.read_last_row()["is_charging"]) else "not charging"
                log_is_afk = "(AFK)" if strbool(self.timelog.read_last_row()["is_afk"]) else ''
                log_cycle = str(self.timelog.read_last_row()["battery_cycle"]) + " cycles"
                if len(self.timelog.data) > 1:
                    self.timelog_file = self.file.name if hasattr(self, "file") else None
                    try:
                        start_time = dt.datetime.fromtimestamp(int(self.timelog.scan_last_N_rows(0, self.timelog_file)[-2]["timestamp"]))
                    except:
                        start_time = dt.datetime.fromtimestamp(int(self.timelog.scan_last_N_rows(0, self.timelog_file)[-1]["timestamp"]))
                    end_time = dt.datetime.fromtimestamp(int(self.timelog.scan_last_N_rows(0, self.timelog_file)[-1]["timestamp"]))
                    time_difference = self.timelog.time_diff(start_time, end_time)
                    self.label.configure(text=f"Battery {'charging' if self.battery.is_charging else 'consumes'} every {time_difference}")
                
                self.battery_log_table.append(f"{log_timestamp} - {log_percent}% | {log_is_charging} {log_is_afk} ({log_cycle})")
                if len(self.battery_log_table) > 5:
                    self.battery_log_table.pop(0)
                self.battery_log_var.set(self.battery_log_table)
                self.l.pack()
                
        try:
            self.afk_set_time = int(self.AFKsecs_box.get())
        except ValueError:
            # if there's non-numeral characters in the spinbox, 
            # loop and append the integers until the next character is non-number
            for i in self.AFKsecs_box.get():
                try:
                    string_int += str(int(i))
                    self.afk_set_time = int(string_int)
                except:
                    break
        self.AFKdetector.afk_time = self.afk_set_time
        if self.AFKdetector.check_if_afk():
            self.isAFK_label.configure(text=f"Yes")
        else:
            self.isAFK_label.configure(text=f"No")
        
        self.AFKtime_label.configure(text=f"{self.afk_set_time} seconds")
        self.master.after(1000, self.reloop)

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = MainWindow(root)
    root.after(2000, my_gui.reloop)
    root.mainloop()