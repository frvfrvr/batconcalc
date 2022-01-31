#!/opt/homebrew/Caskroom/miniforge/base/envs/playground/bin/python3

# ! Battery Consumption Calculator
# ! Author: @frvfrvr (github.com/frvfrvr)
# ! v1 Development Time and Date: Jan-30-2022 6:23 PM - Jan-31-2022 6:34 PM

from tkinter import *
import psutil
import datetime

# ? initiliaze the tkinter window

batthr = []
battmin = []
battsec = []
battpercent = []

def comma_insert(a, b):
    # if another element exists, insert comma
    if bool(a) and bool(b) == True:
        return ", "
    return ""

def batteryConsumption(dt, batthr, battmin, battsec, battpercent, simple=False):
    # requires datetime, battery hours, battery minutes, battery seconds, battery percentage    
    battery = psutil.sensors_battery()
    dthr = int(dt.strftime("%H"))
    dtmin = int(dt.strftime("%M"))
    dtsec = int(dt.strftime("%S"))
    if simple == True:
        # Manually append the new time and battery percentage in case of simple mode
        batthr.append(dthr)
        battmin.append(dtmin)
        battsec.append(dtsec)
        battpercent.append(battery.percent)
    else:
        if battery.power_plugged == False:
            if (battpercent == []) or (len(battpercent) < 2):
                battpercent.append(battery.percent)
                battsec.append(dtsec)
                batthr.append(dthr)
                battmin.append(dtmin)
                return "Calculating... Current battery percentage: " + str(battery.percent) + "%"
            elif (battpercent != []) or (battery.percent < battpercent[-1]):
                if battpercent[-1] != battery.percent:
                    battpercent.append(battery.percent)
                    battsec.append(dtsec) 
                    batthr.append(dthr) 
                    battmin.append(dtmin) 
                # ? MATH PART
                # ? battery life in seconds
                b_sec = battsec[-1] - battsec[-2] if len(battsec) != 0 else 0
                # ? battery life in minutes
                b_min = battmin[-1] - battmin[-2] if len(battmin) != 0 else 0
                # ? battery life in hours
                b_hr = batthr[-1] - batthr[-2] if len(batthr) != 0 else 0
                # ? STRING PART
                # abs() absolute is used to prevent negative values
                ba_hr = str(abs(b_hr)) + " hours" if abs(b_hr) > 1 else str(abs(b_hr)) + " hour" if b_hr == 1 else ""
                ba_min = str(abs(b_min)) + " minutes" if abs(b_min) > 1 else str(abs(b_min)) + " minute" if b_min == 1 else ""
                ba_sec = str(abs(b_sec)) + " seconds" if abs(b_sec) > 1 else str(abs(b_sec)) + " second" if b_sec == 1 else ""
                if len(battpercent) > 2:
                    del battpercent[:-2]
                    del batthr[:-2]
                    del battmin[:-2]
                    del battsec[:-2]
                #print(bool(ba_hr), bool(ba_min), bool(ba_sec))
                #print(comma_insert(ba_hr, ba_min))
                return "Battery consumes 1% every " + ba_hr + comma_insert(ba_hr, ba_min) + ba_min + comma_insert(ba_min, ba_sec) + ba_sec
            return "Data invalid. Anyway here's the current battery percentage: " + str(battery.percent) + "%"
        else:
            #return "Battery is plugged in, can't calculate consumption"
            # will calculate the 1% recharge every x hours, minutes, seconds
            # "Battery charges 1% every x hours, minutes, seconds"
            if (battpercent == []) or (len(battpercent) < 2):
                battpercent.append(battery.percent)
                battsec.append(dtsec)
                batthr.append(dthr)
                battmin.append(dtmin)
                return "Calculating... Current battery percentage: " + str(battery.percent) + "%"
            elif (battpercent != []) or (battery.percent > battpercent[-1]):
                if battpercent[-1] != battery.percent:
                    battpercent.append(battery.percent)
                    battsec.append(dtsec) 
                    batthr.append(dthr) 
                    battmin.append(dtmin) 
                # ? MATH PART
                # ? battery life in seconds
                b_sec = battsec[-1] - battsec[-2] if len(battsec) != 0 else 0
                # ? battery life in minutes
                b_min = battmin[-1] - battmin[-2] if len(battmin) != 0 else 0
                # ? battery life in hours
                b_hr = batthr[-1] - batthr[-2] if len(batthr) != 0 else 0
                # ? STRING PART
                # abs() absolute is used to prevent negative values
                ba_hr = str(abs(b_hr)) + " hours" if abs(b_hr) > 1 else str(abs(b_hr)) + " hour" if b_hr == 1 else ""
                ba_min = str(abs(b_min)) + " minutes" if abs(b_min) > 1 else str(abs(b_min)) + " minute" if b_min == 1 else ""
                ba_sec = str(abs(b_sec)) + " seconds" if abs(b_sec) > 1 else str(abs(b_sec)) + " second" if b_sec == 1 else ""
                if len(battpercent) > 2:
                    del battpercent[:-2]
                    del batthr[:-2]
                    del battmin[:-2]
                    del battsec[:-2]
                return "Battery recharges 1% every " + ba_hr + comma_insert(ba_hr, ba_min) + ba_min + comma_insert(ba_min, ba_sec) + ba_sec
            return "Battery is plugged in, will try to calculate recharging or consumption later"




# ? window appearnce
window = Tk()

window.title("Avg. Battery Consumption")

window.geometry('475x75') # 475x50, x100 only for testing
window.configure(bg='black')
window.attributes('-topmost',True) # window will always be on top for benchmark purposes

lbl = Label(window, fg='#01ff48', justify='center') # placeholder: text="Battery consumes 1% every XXX hours, XXX minutes, XXX seconds"
lbl.grid(column=0, row=0)
lbl.place(relx=.5, rely=.2, anchor="center") # default very center: relx=.5, rely=.5, anchor="center"

# time = Label(window, fg='#01ff48', justify='center')
# time.grid(column=0, row=1)

timelog =  Label(window, fg='#808080', justify='center')
timelog.grid(column=0, row=1)
timelog.place(relx=.5, rely=.60, anchor="center")


    
def my_mainloop():
    dt = datetime.datetime.now()
    battstat = batteryConsumption(dt, batthr, battmin, battsec, battpercent)
    lbl.configure(text=battstat)
    if len(battpercent) > 1:
        logtime = f"{batthr[-1]}:{battmin[-1]}:{battsec[-1]} - {battpercent[-1]}%\n{batthr[-2]}:{battmin[-2]}:{battsec[-2]} - {battpercent[-2]}%"
        timelog.configure(text=logtime)
    
    # ? for testing only
    #dts = dt.strftime("%d-%m-%Y %H:%M:%S %p")
    #batty = psutil.sensors_battery()
    #timelog.configure(text=f"{dts} {batty.percent}% {batthr} {battmin} {battsec} {battpercent}")
    window.after(1000, my_mainloop)    

window.after(1000, my_mainloop)


window.mainloop()