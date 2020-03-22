import subprocess

def levelfunk1(volumelevel): #Sets volumelevel for sysvolume. Uses a diffrent format for the volume value

    volumelevel = int(65535*float(volumelevel))

    try:
        subprocess.run("nircmd.exe setsysvolume %s" % (volumelevel))
    except:
        sleep(1) # wait, probably to many requests

def levelfunk2(volumelevel): #using nircmd to control volume for each application

    try:
        subprocess.run("nircmd.exe setappvolume spotify.exe %s" % (volumelevel))
        subprocess.run("nircmd.exe setappvolume vlc.exe %s" % (volumelevel))
    except:
        sleep(1) # wait, probably to many requests


def levelfunk3(volumelevel): #using nircmd to control volume for each application
    try:
        subprocess.run("nircmd.exe setappvolume /11248 %s" % (volumelevel)) #discord pid 4944 misc audio 11248 voice audio
        subprocess.run("nircmd.exe setappvolume /4944 %s" % (volumelevel))
        subprocess.run("nircmd.exe setappvolume skype.exe %s" % (volumelevel))
    except:
        sleep(1) # wait, probably to many requests


    #can use .Popen insteed removes stutter on volume change

def levelfunk4(volumelevel): #using nircmd to control volume for each application
    try:
        subprocess.run("nircmd.exe setappvolume focused %s" % (volumelevel))
    except:
        sleep(1) # wait, probably to many requests 
