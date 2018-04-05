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

text_file = open('/home/mbshbn/Documents/Motor_Tests/tiger700/v2.txt', 'w')

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
		for i in range(0,10): #enter how long you want it to self correct or "while: 1" for infinite
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
			print ("Command: %i" %command)
			ser.write(str(command).encode())
			time.sleep(1)
		for i in range(0,300):
			ser.flushInput()
			ser.flushOutput()
			for x in range(0, 2):
				line = ser.readline()
			line = ser.readline().decode()
			words = line.split("\t")
			thrust = (m*d*9.81)*(float(words[7])-v1)/(v2-v1)/b
			words[7] = "%0.2f" %thrust
			print (words)
			text_file.write(words)
			time.sleep(0.1)
		ser.close()
