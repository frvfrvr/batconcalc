from pynput import mouse, keyboard
import psutil
import csv
import os, subprocess, platform

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
