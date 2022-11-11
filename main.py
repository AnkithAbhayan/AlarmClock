from tkinter import *
import sys
import pytz
import time
from datetime import datetime
import threading
import pygame

pygame.mixer.init()
pygame.mixer.music.load(
    "C:\\Users\\user\\Downloads\\buzzer_alarm.mp3"
)

def hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

default = hex_from_rgb((90,90,90))

def ringalarmwhenitstime(Gui):
    def dismiss_alarm():
        global stop
        stop = True

        Gui.alarm_info.destroy()
        Gui.alarm_notice.destroy()
        Gui.dismiss_button.destroy()
        Gui.all_alarm_info = Label(Gui.root, text=get_alarm_list(), font=extremely_small_font, fg=default, bg=hex_from_rgb((20,20,20)) )
        Gui.all_alarm_info.grid(row=2, column=0, columnspan=2)
    

    def playringtone(alarm_name):
        global stop
        stop = False
        print("Wake Up!")
        Gui.all_alarm_info.destroy()
        Gui.alarm_notice = Label(Gui.root, font=small_font, text="Alarm is ringing!", fg=hex_from_rgb((0,0,0)), bg=hex_from_rgb((0,255,0)))
        Gui.alarm_notice.grid(row=2, column=0, pady=7, columnspan=2)
        Gui.alarm_info = Label(Gui.root, font=small_font, text=f"Alarm info: {alarm_name}", fg=default, bg=hex_from_rgb((20,20,20)))
        Gui.alarm_info.grid(row=3, column=0, columnspan=2)

        Gui.dismiss_button = Button(Gui.root, font=small_font, text="Dismiss", command=lambda:dismiss_alarm())
        Gui.dismiss_button.grid(row=4, column=0, pady=12, columnspan=2)

        for i in range(60):
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                if stop == True:
                    print("Dismiss button pressed.")
                    sys.exit()
                continue

    for item, value in alarms.items():
        temp = getcurrenttime()[0]
        if item == temp:
            dewit = threading.Thread(target=lambda: playringtone(value))
            dewit.start()
            break

def getcurrenttime():
    test = datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
    temp = time.strptime(str(test), "%H:%M:%S")
    return [time.strftime("%I:%M:%S", temp), time.strftime("%p", temp)]

def get_alarm_list():
    list_of_alarms = "All Alarms:"
    checking_lenghtiest = []
    for key, value in alarms.items():
        checking_lenghtiest.append(value)
    length = len(max(checking_lenghtiest, key=len))

    for key, value in alarms.items():
        list_of_alarms += f"\n{key} AM-  {value}{' '*(length-len(value))}"
    return list_of_alarms

def updaterealtime(Gui):
    current_time = getcurrenttime()
    Gui.timestamp["text"] = current_time[0]
    Gui.am_or_pm["text"] = current_time[1]

    while True:
        temp_var = getcurrenttime()
        if temp_var[0] != current_time[0]:
            current_time=temp_var
            Gui.timestamp["text"] = current_time[0]
            Gui.am_or_pm["text"] = current_time[1]
            ringalarmwhenitstime(Gui)

def togglewindowstate(Gui):
    if Gui.root.attributes('-fullscreen'):
        Gui.root.attributes('-fullscreen', False)
    else:
        Gui.root.attributes('-fullscreen', True)

large_font = ("Fira Code", 150)
medium_font = ("Fira Code", 100)
small_font = ("Fira Code", 25)
extremely_small_font = ("Fira Code", 12)


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.bind("<F11>", lambda event: togglewindowstate(self))

        self.root["bg"] = hex_from_rgb((0,0,0))

        self.info = Label(self.root, text="Ankith's alarm clock.", font=small_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.timestamp = Label(self.root, text="00:00:00", font=large_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.am_or_pm = Label(self.root, text="NN", font=medium_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.all_alarm_info = Label(self.root, text=get_alarm_list(), font=extremely_small_font, fg=default, bg=hex_from_rgb((20,20,20)) )

        self.info.grid(row=0, column=0, pady=50, columnspan=2)
        self.timestamp.grid(row=1, column=0, pady=70, padx=80)
        self.am_or_pm.grid(row=1, column=1)
        self.all_alarm_info.grid(row=2, column=0, columnspan=2)

        self.timeupdate = threading.Thread(target=lambda: updaterealtime(self))
        self.timeupdate.start()


        self.root.mainloop()

Gui = Gui()
