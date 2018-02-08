"""
This code sends a command to the motor based on a desired thrust and the voltage read from the esc.
Before running, run analysis.py and do a force calibration test.
"""

import numpy as np
from scipy.interpolate import griddata
import math
import serial
import string
import time

def getcmd33(volt,thrust):
    p = [149.9370709542070,-9.4262619286830,61.0651814496705,1.0772777426676,-3.5065436563418,-24.2441589620413,0.7259316469796,0.9164650265003,-0.1121752550944,9.1347440241661]
    volt = (volt-11.62)/.6084  #(var-mean)/stddev
    thrust = (thrust-2.505)/1.92
    cmd = p[0] + p[1]*volt + p[2]*thrust + p[3]*volt**2 + p[4]*volt*thrust + p[5]*thrust**2 + p[6]*volt**3 + p[7]*(volt**2)*thrust + p[8]*volt*thrust**2 + p[9]*thrust**3
    return cmd

port = '/dev/ttyACM0'
baud = 9600

m=0.2; d=0.088; b=0.165
# v1=46.2671; v2=130.5342  #Run a force calibration test to determine v values. To input values manually, uncomment this line.
v1_data = np.loadtxt('/home/Documents/robbev1.txt')
v2_data = np.loadtxt('/home/Documents/robbev2.txt')
v1= np.mean(v1_data)
v2= np.mean(v2_data)

points = np.c_[X,Y]

while 1:
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(0.5)
    ser.flushInput()
    ser.flushOutput()
    force = input("Enter the force: ")
    if force == 0:
        time.sleep(1)
        command = 0
        ser.write(str(command))
        time.sleep(0.25)
        ser.close()
    else:
        for i in range(0,5): #enter how long you want it to self correct or "while: 1" for infinite
            ser.flushInput()
            ser.flushOutput()
            for x in range(0, 2):
                line = ser.readline()
            line = ser.readline()
            words = string.split(line,"\t")
            thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
            words[7] = "%0.2f" %thrust
            print words
            voltage = float(words[6])*0.1
            print "Voltage: %0.1f" %voltage
            command = getcmd33(voltage,force)
            print "Command: %i" %command
            ser.write(str(command))
            time.sleep(1)
        while 1:
            ser.flushInput()
            ser.flushOutput()
            for x in range(0, 2):
                line = ser.readline()
            line = ser.readline()
            words = string.split(line,"\t")
            thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
            words[7] = "%0.2f" %thrust
            print words
            time.sleep(0.5)
        ser.close()
