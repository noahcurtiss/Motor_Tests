"""
This code uses interpolation to determine a command given an input voltage and desired force. It is
similar to inputVolt2cmd_send but does not send data to the arduino.
An example code for graphing the results is also shown below.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import math
import serial
import string

B = np.load('/home/Documents/matrix_B.npy')
X = B[:,0]
Y = B[:,2]
Z = B[:,1]

points = np.c_[X,Y]

# Example code for graphing:

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# grid_x, grid_y = np.mgrid[10.7:12.7:40j, 0:max(Y):300j]
# 
# grid_z = griddata(points, Z, (grid_x, grid_y), method='linear')
# 
# print griddata(points, Z, (11.1, 5), method='linear')
# 
# ax.scatter(X,Y,Z,'o')
# ax.plot_wireframe(grid_x,grid_y, grid_z, rstride=1, cstride=1)
# plt.show()

voltage = input("Enter voltage: ")
print "The voltage is %f" %voltage

while 1:
	force = input("Enter the force: ")
	print "The force is %f" %force
	command = int(griddata(points, Z, (voltage, force), method='linear'))
	print "Command: %i" %command