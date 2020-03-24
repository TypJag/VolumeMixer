from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess


def setAppVolumeName(appName, level):
    try:
        sessions = AudioUtilities.GetAllSessions() #get an object
        for session in sessions: #for each nested object
            if session.Process and session.Process.name() == appName: #check if it is object we seek
                volume = session.SimpleAudioVolume #get object from object
                volume.SetMasterVolume(level, None) #use a method from object to change volyme
    except:
        pass

def setAppVolumePid(pid, level):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.ProcessId == pid:
                volume.SetMasterVolume(level, None)
    except:
        pass

def setSystemVolume(level):
    try:
        #do know
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)
    except:
        pass
