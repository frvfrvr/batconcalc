import csv
import datetime as dt
import time
import os, subprocess, platform
import psutil
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfile
from pynput import mouse, keyboard

class TimeLog:
    def __init__(self):
        self.headers = ["timestamp", "battery_percent", "is_charging", "is_afk", "battery_cycle"]
        self.data = []
    
    def csv_create(self, file_name):
        self.file_name = file_name
        # check if contents of csv file is empty and if not empty, check headers and append latest data rows
        if os.stat(self.file_name).st_size == 0:
            with open(self.file_name, "a+") as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                # write each row from self.data to csv file
                try:
                    for row in self.data:
                        writer.writerow(row)
                except:
                    pass
        else:
            # check headers
            # replace the headers of csv file with the new headers from self.headers
            with open(self.file_name, "r") as f:
                old_data = f.readlines()
                old_data[0] = ",".join(self.headers) + "\n"
                # prev_data for joining new self.data and prev_data together later
                prev_data = [i for i in self.data]
                # clear self.data
                self.data = []
                # using dictionary method
                reader = csv.DictReader(open(self.file_name), fieldnames=self.headers)
                # change self.data to rows in csv file without header
                self.data = list(reader)[1:]
                    #self.data.append(row)
                for row in reader:
                    if row["timestamp"] != "timestamp":
                        self.data.append(row)
                # merge prev_data and self.data with prev_data being after self.data
                self.data = self.data + prev_data
            with open(self.file_name, "w") as f:
                f.writelines(old_data)
    
    def csv_append(self, content):
        with open(self.file_name, "a") as f:
            # writer dictionary to csv using DictWriter
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(content)
    
    def csv_open(self):
        # open csv file in default program
        if platform.system() == 'Darwin':
            subprocess.call(('open', self.file_name))
        elif platform.system() == 'Windows':
            os.startfile(self.file_name)
        else:
            subprocess.call(('xdg-open', self.file_name))
    
    def update(self, timestamp, battery_percent, is_charging: bool, is_afk: bool, battery_cycle = 0):
        if platform.system() == 'Darwin':
            self.data.append({"timestamp": int(timestamp), "battery_percent": battery_percent, "is_charging": is_charging, "is_afk": is_afk, "battery_cycle": battery_cycle})
        else:
            self.data.append({"timestamp": int(timestamp), "battery_percent": battery_percent, "is_charging": is_charging, "is_afk": is_afk})
        if hasattr(self, 'file_name'):
            # csv_append in dictionary format
            if platform.system() == 'Darwin':
                self.csv_append({"timestamp": int(timestamp), "battery_percent": battery_percent, "is_charging": is_charging, "is_afk": is_afk, "battery_cycle": battery_cycle})
            else:
                self.csv_append({"timestamp": int(timestamp), "battery_percent": battery_percent, "is_charging": is_charging, "is_afk": is_afk})
    
    # read last row in csv file in dictionary format
    def read_last_row(self):
        try:
            if hasattr(self, 'file_name'):
                with open(self.file_name, "r") as f:
                    reader = csv.DictReader(f, fieldnames=self.headers)
                    last_row = list(reader)[-1]
                    if last_row["timestamp"] == "timestamp":
                        last_row = list(reader)[-2]
                    return last_row
            else:
                return self.data[-1]
        except:
            return None
        
    # return last N rows in csv file in dictionary format
    def read_last_N_rows(self, N, filename = None):
        try:
            if filename:
                with open(filename, "r") as f:
                    reader = csv.DictReader(f, fieldnames=self.headers)
                    last_N_rows = list(reader)[-N:]
                    # if it included header row, remove it
                    if last_N_rows[0]["timestamp"] == "timestamp":
                        last_N_rows.pop(0)
                    if len(last_N_rows) < 1:
                        return self.read_last_row()
                    return last_N_rows
            else:
                return self.data[-N:]
        except:
            return None
    
    # scan last N rows for battery percent and last timestamp for each battery percent and return a dictionary
    # key is battery percent, value is timestamp
    # if same battery percent is found, return the latest timestamp
    # if different battery percent is found, create new key and value
    # finally, return a list of dictionaries with key as battery percent and value as timestamp
    def scan_last_N_rows(self, N, filename = None):
        last_N_rows = self.read_last_N_rows(N, filename)
        if last_N_rows:
            # create a dictionary with key as battery percent and value as timestamp
            # if same battery percent is found, return the latest timestamp
            # if different battery percent is found, create new key and value
            battery_percent_timestamp_dict = {}
            for row in last_N_rows:
                battery_percent_timestamp_dict[row["battery_percent"]] = row["timestamp"]
            # return a list of dictionaries with key as battery percent and value as timestamp
            # return battery_percent_timestamp_dict
            # insert each percent timestamp dict pair into a list
            battery_percent_timestamp_list = []
            for key, value in battery_percent_timestamp_dict.items():
                # battery_percent_timestamp_list.append({key: value})
                # {battery_percent: key, timestamp: value}
                battery_percent_timestamp_list.append({"battery_percent": key, "timestamp": value})
            battery_percent_timestamp_list = sorted(battery_percent_timestamp_list, key=lambda d: d['timestamp'])
            return battery_percent_timestamp_list
        else:
            return None
    
    # check last row in csv file and compare to current data
    # if last row values are different, append new row. else return False
    # True means last row values is same as input parameters
    # False means last row values is different from input parameters
    def check_last_row(self, battery_percent, is_charging: bool, is_afk: bool, percent_only=False):
        # check if last row data's values are the same as current data
        for k, v in self.data[-1].items():
            if k == "timestamp":
                pass
            if k == "battery_percent":
                if v != battery_percent:
                    return False
                else:
                    pass
            if not percent_only:
                if k == "is_charging":
                    if v != is_charging:
                        return False
                    else:
                        pass
                if k == "is_afk":
                    if v != is_afk:
                        return False
                    else:
                        pass
        return True
    
    @staticmethod
    def time_diff(start_time, end_time):
        plural = lambda value: "s" if value > 1 else ""
        diff = end_time - start_time
        # days
        days = diff.days
        # hours
        # hours = diff.seconds // 3600
        hours, remainder = divmod(diff.seconds, 3600)
        # minutes
        # minutes = (diff.seconds // 60) % 60
        minutes, seconds = divmod(remainder, 60)
        # seconds
        # seconds = diff.seconds % 600
        # return as string
        if days > 0:
            return f"{days} day{plural(days)}, {hours} hour{plural(hours)}, {minutes} minute{plural(minutes)}, and {seconds} second{plural(seconds)}"
        elif hours > 0:
            return f"{hours} hour{plural(hours)}, {minutes} minute{plural(minutes)}, and {seconds} second{plural(seconds)}"
        elif minutes > 0:
            return f"{minutes} minute{plural(minutes)} and {seconds} second{plural(seconds)}"
        elif seconds > 0:
            return f"{seconds} second{plural(seconds)}"
        else:
            return f"0 second"
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return f"{seconds} second{plural(seconds)}"
                else:
                    return f"{minutes} minute{plural(minutes)}, {seconds} second{plural(seconds)}"
            else:
                return f"{hours} hour{plural(hours)}, {minutes} minute{plural(minutes)}, {seconds} second{plural(seconds)}"
        else:
            return f"{days} day{plural(days)}, {hours} hour{plural(hours)}, {minutes} minute{plural(minutes)}, {seconds} second{plural(seconds)}"

class BatteryState:
    def __init__(self):
        self.battery = psutil.sensors_battery()
        if platform.system() == 'Darwin':
            self.cycle_count = int(subprocess.check_output("system_profiler SPPowerDataType | grep 'Cycle Count' | awk '{print $3}'", shell=True).strip().decode("utf-8"))
        else:
            self.cycle_count = 0
        self.is_charging = self.battery.power_plugged
        self.percent = self.battery.percent
        
    def update(self):
        self.battery = psutil.sensors_battery()
        if platform.system() == 'Darwin':
            self.cycle_count = int(subprocess.check_output("system_profiler SPPowerDataType | grep 'Cycle Count' | awk '{print $3}'", shell=True).strip().decode("utf-8"))
        else:
            self.cycle_count = 0
        self.is_charging = self.battery.power_plugged
        self.percent = self.battery.percent

class AFKdetector:
    def __init__(self, afk_time = 20) -> None:
        self.afk_time = afk_time
        self.start_afk = int(time.time())
        self.is_afk = False
        self.already_afk = False
        self.x, self.y = 0, 0
        self.prev_x, self.prev_y = 0, 0
        self.is_active = False
    
    # for mouse
    def on_move(self, x, y):
        self.x, self.y = x, y
        self.start_afk = int(time.time())
        self.is_afk = False
        
    def on_click(self, x, y, button, pressed):
        self.is_active = True if pressed else False
        self.x, self.y = x, y
        self.start_afk = int(time.time())
        self.is_afk = False
        
    def on_scroll(self, x, y, dx, dy):
        self.is_active = True if dx > -1 or dy > -1 else False
        self.x, self.y = x, y
        self.start_afk = int(time.time())
        self.is_afk = False
        
    # for keyboard
    def on_press_release(self, key):
        self.is_active = True if key else False
        self.start_afk = int(time.time())
        self.is_afk = False

    # check if user is afk
    def check_if_afk(self):
        self.afkcount = int(time.time()) - self.start_afk
        if self.already_afk:
            if self.x != self.prev_x or self.y != self.prev_y or self.is_active:
                self.already_afk = False
                self.is_afk = False
                self.is_active = False
                return False
            elif self.prev_x == self.x and self.prev_y == self.y:
                self.is_afk = True
                self.already_afk = True
                return True
        else:
            if int(time.time()) - self.start_afk > self.afk_time:
                self.prev_x, self.prev_y = self.x, self.y
                self.is_afk = True
                self.already_afk = True
                return True
            return False
        
    # start the listener
    def start(self, blocking=False):
        if blocking:
            with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as self.MouseListener, keyboard.Listener(
                on_press=self.on_press_release,
                on_release=self.on_press_release) as self.KeyboardListener:
                self.MouseListener.join()
                self.KeyboardListener.join()
                
        else:
            self.MouseListener= mouse.Listener(
                    on_move=self.on_move,
                    on_click=self.on_click,
                    on_scroll=self.on_scroll)
            self.KeyboardListener = keyboard.Listener(
                    on_press=self.on_press_release,
                    on_release=self.on_press_release)
            self.KeyboardListener.start()
            self.MouseListener.start()

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