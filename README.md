# VolumeMixer
A python script and arduino code for a hardware volume mixer for programs running on a Windows system

Link to a gallery of the project: https://www.sweclockers.com/galleri/15041-volymmixer

The hardware used is a simple arduino nano clone. 

Some modifications of the python script might be required for it to work with another arduino. In the findarduinoNano function there is a int called pid which is used to identifi COM-port the arduino is connected to. More intructions is in the comments in the script.

The shortcut needs to be uppdated with the correct path to the python script and the python install directory.

Some packages are needed to run the python script. More info in the script.

The arduino code requires bounce2.h. https://github.com/thomasfredericks/Bounce2

This project uses nircmd.exe by NirSoft https://www.nirsoft.net/utils/nircmd.html

