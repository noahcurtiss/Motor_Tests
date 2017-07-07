"""
This code sends a command to the motor given an input voltage and desired force
"""

import numpy as np
from scipy.interpolate import griddata
import math
import serial

port = '/dev/ttyACM0'
baud = 9600


B = np.load('/home/Documents/matrix_B.npy')
X = B[:,0]
Y = B[:,2]
Z = B[:,1]

points = np.c_[X,Y]

voltage = input("Enter voltage: ")
print "The voltage is %f" %voltage

while 1:
	ser = serial.Serial(port, baud, timeout=1)
	force = input("Enter the force: ")
	if force == 0:
		command = 0
	else:
		command = int(griddata(points, Z, (voltage, force), method='linear'))
	print "Command: %i" %command
	ser.write(str(command))
	ser.close()
	# while 1:
	# 	a = ser.read()
	# 	print a
