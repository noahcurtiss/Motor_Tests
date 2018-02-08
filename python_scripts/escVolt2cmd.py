"""
This code simulates escVolt2cmd_send.py without sending data to the arduino. Given the input voltage
and desired force, it determines a command and the corresponding voltage change. Useful for determining
the number of loops required for the command to settle.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import math
import serial
import string

C = np.load('/home/noah/Documents/matrix_C.npy')
D = np.load('/home/noah/Documents/matrix_D.npy')

X = C[:,0]
Y = C[:,2]
Z = C[:,1]

X1 = D[:,0]
Y1 = D[:,1]
Z1 = D[:,2] 

points = np.c_[X,Y]
points1 = np.c_[X1,Y1]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# grid_x, grid_y = np.mgrid[10.7:12.7:40j, 0:max(Y):300j]

# grid_z = griddata(points, Z, (grid_x, grid_y), method='linear')

# print griddata(points, Z, (11.1, 5), method='linear')

# ax.scatter(X,Y,Z,'o')
# ax.plot_wireframe(grid_x,grid_y, grid_z, rstride=1, cstride=1)
# plt.show()

voltage1 = input("Enter the input voltage: ")
force = input("Enter the force: ")
voltage = voltage1
for i in range(0,5):
	command = int(griddata(points, Z, (voltage, force), method='linear'))
	print "Command: %i" %command
	voltage = griddata(points1, Z1, (voltage1, command), method='linear')
	print "voltage: %0.1f" %voltage