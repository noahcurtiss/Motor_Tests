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

def escvolt_filter(A,escvolt):
    voltMatrix = np.zeros(12)
    for line in A:
        if (round(line[6],1) == escvolt):
            voltMatrix = np.vstack((voltMatrix,line))
    voltMatrix = np.delete(voltMatrix,(0),axis=0)
    return voltMatrix

total_data = np.load('/home/noah/Documents/total_data.npy')
voltage_values = [10.6,11.3,12.0,12.6]
cmddata = np.zeros(4)

force = 2
i=0

for volt in voltage_values:
    voltdata = escvolt_filter(total_data,volt)

    force_data = voltdata[:,10]
    cmd_data = voltdata[:,0]

    fit = np.polyfit(force_data,cmd_data,2)
    f = np.poly1d(fit)

    cmddata[i] = f(force)
    i+=1
fitout = np.polyfit(voltage_values,cmddata,2)
fout = np.poly1d(fitout)


for i in range(0,5): #enter how long you want it to self correct or "while: 1" for infinite
    voltage = 11.1
    print "Voltage: %0.1f" %voltage
    cmdout = fout(voltage)
    print "Command: %i" %cmdout