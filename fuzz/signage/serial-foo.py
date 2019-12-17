import serial
ser_data=''

ser=serial.Serial('/dev/ttyUSB0', 115200)
print(ser.name)

ser.write(b'hello world')

while(1):
    ser_data = ser.readline()   
    print(ser_data)
    ser_data.strip(b'\r').strip(b'\n')   
    print(ser_data)

    if b'foo' in ser_data:
        print("food received")
        ser.close()
        break

print("end")
