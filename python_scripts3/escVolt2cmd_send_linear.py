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

port = '/dev/ttyACM0'
baud = 9600

m=0.5; d=0.088; b=0.084
# v1=46.2671; v2=130.5342  #Run a force calibration test to determine v values. To input values manually, uncomment this line.
v1_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v1.txt')
v2_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v2.txt')
v1= np.mean(v1_data)
v2= np.mean(v2_data)

total_data = np.load('/home/mbshbn/Documents/Motor_Tests/tiger700/total_data.npy')
voltage_values = [14.4,14.6,14.8,15.2]
cmddata = np.zeros(4)

while 1:
	ser = serial.Serial(port, baud, timeout=1)
	time.sleep(0.5)
	ser.flushInput()
	ser.flushOutput()
	force = float(input("Enter the force: "))
	if force == 0:
		time.sleep(1)
		command = 0
		ser.write(str(command).encode())
		time.sleep(0.25)
		ser.close()
	else:
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
			ser.flushInput()
			ser.flushOutput()
			for x in range(0, 20):
				line = ser.readline()
			line = ser.readline().decode()
			words = line.split("\t")
			thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
			words[7] = "%0.2f" %thrust
			print(words)
			voltage = float(words[6])*0.1
			print ("Voltage: %0.1f" %voltage)
			cmdout = fout(voltage)
			print ("Command: %i" %cmdout)
			ser.write(str(int(cmdout)).encode())
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
			print(words)
			time.sleep(0.5)
		ser.close()
