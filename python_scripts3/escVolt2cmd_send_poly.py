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

def getcmd33(x,y): # x = volt, y=thrust
    # p = [149.9370709542070,-9.4262619286830,61.0651814496705,1.0772777426676,-3.5065436563418,-24.2441589620413,0.7259316469796,0.9164650265003,-0.1121752550944,9.1347440241661]
    # volt = (volt-11.62)/.6084  #(var-mean)/stddev
    # thrust = (thrust-2.505)/1.92
    # cmd = p[0] + p[1]*volt + p[2]*thrust + p[3]*volt**2 + p[4]*volt*thrust + p[5]*thrust**2 + p[6]*volt**3 + p[7]*(volt**2)*thrust + p[8]*volt*thrust**2 + p[9]*thrust**3
    p00 = 101.1  
    p10 = -6.701
    p01 = 38.26 
    p11 = 0.9139  
    p02 = -1.081  
    p12 = -0.2883
    p03 = 0.2441 

    cmd = p00 + p10*x + p01*y + p11*x*y + p02*y**2+ p12*x*y**2 + p03*y**3
    return cmd

port = '/dev/ttyACM0'
baud = 9600

m=0.5; d=0.088; b=0.084
# v1=46.2671; v2=130.5342  #Run a force calibration test to determine v values. To input values manually, uncomment this line.
v1_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v1.txt')
v2_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v2.txt')
v1= np.mean(v1_data)
v2= np.mean(v2_data)

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
        for i in range(0,15): #enter how long you want it to self correct or "while: 1" for infinite
            ser.flushInput()
            ser.flushOutput()
            for x in range(0, 2):
                line = ser.readline()
            line = ser.readline().decode()
            words = line.split("\t")
            thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
            words[7] = "%0.2f" %thrust
            print (words)
            voltage = float(words[6])*0.1
            print ("Voltage: %0.1f" %voltage)
            command = getcmd33(voltage,float(force))
            print ("Command: %i" %command)
            ser.write(str(int(command)).encode())
            time.sleep(1)
        while 1:
            ser.flushInput()
            ser.flushOutput()
            for x in range(0, 2):
                line = ser.readline()
            line = ser.readline().decode()
            words = line.split("\t")
            thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
            words[7] = "%0.2f" %thrust
            print (words)
            time.sleep(0.5)
        ser.close()
