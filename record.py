"""
This code records serial data as an array of strings
"""

import serial

connected = False

location='/dev/ttyACM0'

ser = serial.Serial(location, 9600)

## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True
   
text_file = open('/home/Documents/robbev2.txt', 'w') #name of target file
#recommended file name format: <path><motor><input_voltage><type>.txt
#(type: v1, v2, nothing, etc)

while 1:
    if ser.inWaiting():
        x=ser.read()
        print(x) 
        text_file.write(x)
text_file.close()
ser.close()
