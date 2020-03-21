from infi.systray import SysTrayIcon
import serial
import serial.tools.list_ports
import os
import ctypes
import subprocess
import codecs
import win32ui
import win32api
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY
from infi.systray import SysTrayIcon

#packages needed to be installed with pip
#infi.systray
#pyserial
#pywin32


#Finds local dir for nircmd.exe
os.chdir(os.path.dirname(os.path.realpath(__file__)))


shouldIQuit = False


def on_quit(systray): #What happens when quit is pressed in the taskbar
    global shouldIQuit
    shouldIQuit = True

def on_about(systray): #About tab
    ctypes.windll.user32.MessageBoxW(None, u"A program that communicates with a dedicated volume mixer \nWriten by Axel Andersson 2020 ", u"About", 0)

def levelfunk1(volumelevel): #using nircmd to control volume for each application
    subprocess.Popen("nircmd.exe setappvolume spotify.exe %s" % (volumelevel))
    subprocess.Popen("nircmd.exe setappvolume vlc.exe %s" % (volumelevel))
    return

def levelfunk2(volumelevel): #using nircmd to control volume for each application
    subprocess.Popen("nircmd.exe setappvolume /11248 %s" % (volumelevel)) #discord pid 4944 misc audio 11248 voice audio
    subprocess.Popen("nircmd.exe setappvolume /4944 %s" % (volumelevel))
    subprocess.Popen("nircmd.exe setappvolume skype.exe %s" % (volumelevel))
    return

def levelfunk3(volumelevel): #using nircmd to control volume for each application
    subprocess.Popen("nircmd.exe setappvolume focused %s" % (volumelevel))
    return

def levelfunk0(volumelevel): #Sets volumelevel for sysvolume. Uses a diffrent format for the volume value

    volumelevel = float(volumelevel)
    floatyThing = 65535*volumelevel
    volumelevel = int(floatyThing)

    subprocess.Popen("nircmd.exe setsysvolume %s" % (volumelevel))
    return

def nextTrack():
    win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
    return

def pauseTrack():
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    return

def prevTrack():
    win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
    return

# def checkWindow(windowName, application, volumelevel):
#     try:
#         win32ui.FindWindow(None, windowName)
#     except win32ui.error:
#         return
#     else:
#         subprocess.Popen("nircmd.exe setappvolume " + application + " %s" % (volumelevel), shell=True)
#         print (application)
#         return
#     return

def findArduinoNanoPort(): #Finds the comport the arduino is connected to
    pidNano = 29987
    #product id. Unique for diffrent kind of devices might be needed to be modified. Use following the following code to find pid
    #portList = list(serial.tools.list_ports.comports())

    # for port in portList:
    #     print(port.pid)

    comport =''

    portList = list(serial.tools.list_ports.comports())

    for port in portList:
        if port.pid == 29987:
            comport = port.device

    return(comport)

def startTrayIcon(): #Starts systemtray icon
    icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Volume mixer icon.ico")

    shutdown_called = False #Do know

    menu_options = (("About", None, on_about),)
    systray = SysTrayIcon(icon_path, "Volume Mixer", menu_options, on_quit)
    systray.start()

    return

startTrayIcon()


serialport = serial.Serial(findArduinoNanoPort())

while True:
    arduinostring = serialport.readline()
    workingString = arduinostring.split( )

    if workingString[0].decode('utf-8') == "1": #Spotify
        levelfunk1(workingString[1].decode('utf-8'))
    if workingString[0].decode('utf-8') == "2": #Discord/Skype
        levelfunk2(workingString[1].decode('utf-8'))
    if workingString[0].decode('utf-8') == "3": #Focused on
        levelfunk3(workingString[1].decode('utf-8'))
    if workingString[0].decode('utf-8') == "0": #Systemsound
        levelfunk0(workingString[1].decode('utf-8'))
    if workingString[0].decode('utf-8') == "4": #Pause/play, next and previous track
        if workingString[1].decode('utf-8') == "0":
            prevTrack()
        if workingString[1].decode('utf-8') == "1":
            pauseTrack()
        if workingString[1].decode('utf-8') == "2":
            nextTrack()

    if shouldIQuit == True: #Making the program stop if quit is used in the system tray
      break
