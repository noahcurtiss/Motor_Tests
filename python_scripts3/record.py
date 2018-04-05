"""
This code records serial data as an array of strings
"""

import serial
import time

connected = False

location='/dev/ttyACM0'

ser = serial.Serial(location, 9600, timeout=1)

## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True
   
text_file = open('/home/mbshbn/Documents/Motor_Tests/tiger700/v1.txt', 'w') #name of target file
#recommended file name format: <path><motor><input_voltage><type>.txt
#(type: v1, v2, nothing, etc)

start_time = time.time()
while 1:
    if ser.inWaiting():
        x=ser.readline().decode()
        #elapsed_time = time.time()-start_time
        #string = x.strip()+'\t'+str(elapsed_time) +'\n'
        print(x)
        text_file.write(x)
text_file.close()
ser.close()
