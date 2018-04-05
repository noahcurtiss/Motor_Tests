"""
This code sends a command to the motor based on a desired thrust and the voltage read from the esc.
Before running, run analysis.py and do a force calibration test.
"""

import numpy as np
from scipy.interpolate import griddata, interp1d
import math
import serial
import string
import time

port = '/dev/ttyACM0'
baud = 9600

m=0.5; d=0.088; b=0.084
# v1=46.2671; v2=130.5342  #Run a force calibration test to determine v values. To input values manually, uncomment this line.
v1_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v1.txt')
v2_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/v2.txt')
v1= np.mean(v1_data)
v2= np.mean(v2_data)

C = np.load('/home/mbshbn/Documents/Motor_Tests/tiger700/matrix_C.npy')
X = C[:,0]
Y = C[:,2]
Z = C[:,1]

points = np.c_[X,Y]

f =interp1d(Y,Z)

text_file = open('/home/mbshbn/Documents/Motor_Tests/tiger700/test2.txt', 'w')

for force in [0.5,1,2,3,4,5,6,7,8,9]:
	ser = serial.Serial(port, baud, timeout=1)
	time.sleep(0.5)
	ser.flushInput()
	ser.flushOutput()
	if force == 0:
		time.sleep(1)
		command = 0
		ser.write(str(command))
		time.sleep(0.25)
		ser.close()
	else:
		for i in range(0,7): #enter how long you want it to self correct or "while: 1" for infinite
			ser.flushInput()
			ser.flushOutput()
			for x in range(0, 10):
				line = ser.readline()
			line = ser.readline().decode()
			words = line.split("\t")
			thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
			words[7] = "%0.2f" %thrust
			print (words)
			voltage = float(words[6])*0.1
			print ("Voltage: %0.1f" %voltage)
			command = int(griddata(points, Z, (voltage, force), method='linear'))
			#command = int(f(force))
			print ("Command: %i" %command)
			ser.write(str(command).encode())
			time.sleep(1)
		for i in range(0,100):
			ser.flushInput()
			ser.flushOutput()
			for x in range(0, 2):
				line = ser.readline()
			line = ser.readline().decode()
			words = line.split("\t")
			thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
			string = line.rstrip() +"\t"+str(thrust)+"\t"+str(force)+"\n"
			print(string)
			text_file.write(string)
			time.sleep(0.05)
time.sleep(1)
command = 0
ser.write(str(command).encode())
time.sleep(0.25)
ser.close()