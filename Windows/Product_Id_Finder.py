import serial
import serial.tools.list_ports

portList = list(serial.tools.list_ports.comports())

for port in portList:
     print(port.pid)