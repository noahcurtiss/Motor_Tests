"""
This code takes data collected from the step tests, cleans it up and compiles it into a
matrix with all the edited data (total_data) and three matricies used for graphing and
interpolation. The output is a .npy and a .txt file for each matrix.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import math
import serial
import string

path = '/home/mbshbn/Documents/Motor_Tests/tiger700/'

def bitfilter(matrix):    #filters out all maxPWM values that are not 255
	matrix2 = np.zeros(12)
	sz = np.shape(matrix)
	for i in range(0,sz[0]):
		if matrix[i,2] == 255 and matrix[i,1] != 25.5:
			matrix2 = np.r_['0,2',matrix2,matrix[i]]
	matrix2 = np.delete(matrix2,(0),axis=0)
	return matrix2

def rpmfilter(matrix,minrpm):   #filters out all rpms less than minrpm
	matrix2 = np.zeros(12)      #helpful for lower commands when it takes a while to reach peak speed
	sz = np.shape(matrix)
	for i in range(0,sz[0]):
		if matrix[i,4] >= minrpm:
			matrix2 = np.r_['0,2',matrix2,matrix[i]]
	matrix2 = np.delete(matrix2,(0),axis=0)
	return matrix2

def forcefilter(matrix, risetime, cmd_bounds):   #only includes data after risetime due to lag on force sensor
	matrix2 = np.zeros(12)
	for cmd in range(cmd_bounds[0],cmd_bounds[2]+cmd_bounds[1],cmd_bounds[1]):
		cmd_matrix = matrix[matrix[:,0] == cmd]
		matrix2 = np.r_['0,2',matrix2,cmd_matrix[risetime:]]
	matrix2 = np.delete(matrix2,(0),axis=0)
	return matrix2

def analysis(volt,cmd_bounds):
	#fill in your own file name
	A = np.loadtxt(path+('%.1f' % volt)+ '.txt',delimiter='\t')
	v1_data = np.loadtxt(path+('%.1f' % volt)+ 'v1.txt')
	v2_data = np.loadtxt(path+('%.1f' % volt)+ 'v2.txt')
	
	v1 = np.mean(v1_data)
	v2 = np.mean(v2_data) 	#v1=strain sensor reading with no mass, v2=reading with mass.
	
	force_risetime = 130
	sz = np.shape(A)
	num = range(sz[0])
	
	numMagnets = 12
	rpm = A[:,4]*780/numMagnets
	
	m = 0.5; d = .088; b = .084
	#m=added mass(kg), d=distance of mass to pivot(m), b=distance of motor to pivot(m),
	thrust = (m*d*9.81)*(A[:,7]-v1)/(v2-v1)/b
	v_input = np.full((sz[0],1),volt)
	
	A = np.c_[A,num,rpm,thrust,v_input]
	
	A[:,1] = A[:,1]*0.1
	A[:,6] = A[:,6]*.1
	
	#0:cmd 1:current 2:maxPWM 3:temp 4:rawRPM 5:reserved1 6:voltage 7:rawForce
	#8:count 9:RPM 10:thrust 11:inputVoltage
	
	data = bitfilter(A)
	data = rpmfilter(data,10)
	
	forcedata = forcefilter(data,force_risetime,cmd_bounds)

	for cmd in range(10,260,10):
		if any(abs(cmd - forcedata[:,0])<0.01):
			cmd_matrix = forcedata[abs(forcedata[:,0]-cmd)<0.01]
			avg = np.mean(cmd_matrix[:,7])
			plt.figure(1)
			plt.scatter(cmd_matrix[:,8],cmd_matrix[:,7],marker='.')
			plt.axhline(y=avg)
			plt.ylabel('force')
			plt.title(str(cmd))
			plt.show()
	# plt.figure(1)
	# plt.plot(forcedata[:,6])
	# plt.title('current over an entire test')
	# plt.ylabel('current')
	# plt.show()
	return forcedata

cmd_bounds = [10, 10, 250] #[min_cmd, cmd_step, max_cmd]
volt_range = [10.8,0.2,12.6] #[min input_voltage, imput_voltage step, max input_voltage]
total_data = np.zeros(12)

volt = 14.8
forcedata = analysis(volt,cmd_bounds)
total_data = np.r_['0,2',total_data,forcedata]

total_data = np.delete(total_data,(0),axis=0)