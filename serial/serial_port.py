import serial.tools.list_ports as sp

list = sp.comports()
connected=[]
for i in list:
    connected.append(i.device)

print("Connected COM ports: " + str(connected))

