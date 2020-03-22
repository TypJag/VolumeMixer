from infi.systray import SysTrayIcon
import serial
import serial.tools.list_ports
import os
import ctypes
import codecs
import win32ui
import win32api
from infi.systray import SysTrayIcon
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY
import nircmdcalls

#Script for controling the volume for indvidual programs where the volume is
#controled by a arduino communicating using serial. pidNano might be needed to
#be changed to make the script work.
#By Axel Andersson 2020

#Script is developed for python 3.8.1
#packages needed to be installed with pip
#infi.systray
#pyserial
#pywin32

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
        sleep(1)
        serialport = serial.Serial(findArduinoNanoPort(pidNano))
        continue

    try:
        arduinoStringParts = arduinostring.decode('utf-8').split()
        channel = arduinoStringParts[0]
        value = arduinoStringParts[1]
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
        nircmdcalls.levelfunk1(value)
    elif channel == "2": #Spotift Vlc
        nircmdcalls.levelfunk2(value)
    elif channel == "3": #Discord/Skype
        nircmdcalls.levelfunk3(value)
    elif channel == "4": #Focused on
        nircmdcalls.levelfunk4(value)
