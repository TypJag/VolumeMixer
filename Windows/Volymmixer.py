from infi.systray import SysTrayIcon
import serial
import serial.tools.list_ports
import os
import ctypes
import codecs

import win32ui
import win32gui
import win32api
import win32process
from time import sleep
from infi.systray import SysTrayIcon
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY
import pycawcalls

#Script for controling the volume for indvidual programs where the volume is
#controled by a arduino communicating using serial. pidNano might be needed to
#be changed to make the script work.
#By Axel Andersson 2020

#Script is developed for python 3.8.1
#packages needed to be installed with pip
#infi.systray
#pyserial
#pywin32
#pycaw https://github.com/AndreMiras/pycaw more install instructions in the readme

shouldIQuit = False #

pidNano = 29987 #product id for the arduino nano which is used to identify the correct COM-port
#product id. Unique for diffrent kind of devices might be needed to be modified. Use following the following code to find pid
#portList = list(serial.tools.list_ports.comports())

# for port in portList:
#     print(port.pid)
#Finds local dir for nircmd.exe
#os.chdir(os.path.dirname(os.path.realpath(__file__)))

def on_quit(systray): #What happens when quit is pressed in the taskbar
    global shouldIQuit
    shouldIQuit = True

def on_about(systray): #About tab
    ctypes.windll.user32.MessageBoxW(None, u"A program that communicates with a dedicated volume mixer \nWriten by Axel Andersson 2020 ", u"About", 0)

def startTrayIcon(): #Starts systemtray icon
    icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Volume mixer icon.ico")

    shutdown_called = False #Do know

    menu_options = (("About", None, on_about),)
    systray = SysTrayIcon(icon_path, "Volume Mixer", menu_options, on_quit)
    systray.start()

def nextTrack():
    win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)

def pauseTrack():
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)

def prevTrack():
    win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)



def findArduinoNanoPort(pidNano): #Finds the comport the arduino is connected to
    comport =''

    portList = list(serial.tools.list_ports.comports()) #Gets info about devices connected

    for port in portList: #for each devices connected
        if port.pid == pidNano:
            comport = port.device

    return(comport)

startTrayIcon()

serialport = serial.Serial(findArduinoNanoPort(pidNano))


while not shouldIQuit:
    try:
        arduinostring = serialport.readline(128)
            #print(arduinostring)
    except:
        # Wait and restart serialport and go on
        time.sleep(10)
        serialport = serial.Serial(findArduinoNanoPort(pidNano))
        continue

    try:
        arduinoStringParts = arduinostring.decode('utf-8').split()
        channel = arduinoStringParts[0]
        value = float(arduinoStringParts[1])
    except:
        # Corrupt command, drop it and move on
        continue

    if channel == "0": #Pause/play, next and previous track
        if value == "0":
            prevTrack()
        elif value == "1":
            pauseTrack()
        elif value == "2":
            nextTrack()
    elif channel == "1": #Systemsound
        pycawcalls.setSystemVolume(value)
    elif channel == "2": #Spotift Vlc
        pycawcalls.setAppVolumeName('Spotify.exe', value)
        pycawcalls.setAppVolumeName('vlc.exe', value)
        #nircmdcalls.levelfunk2(value)
    elif channel == "3": #Discord/Skype
        pycawcalls.setAppVolumeName('Discord.exe', value) #discord pid 4944 misc audio 11248 voice audio
        pycawcalls.setAppVolumeName('skype.exe', value)
    elif channel == "4": #Focused on
        window = win32gui.GetForegroundWindow() #Gets a handle on the foregroundwindow
        pids = win32process.GetWindowThreadProcessId(window) #uses the handle to get pid
        for pid in pids: #some programs have more then one pid
            pycawcalls.setAppVolumePid(pid, value)
