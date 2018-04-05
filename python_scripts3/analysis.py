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
	
	print(volt)

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
	return forcedata

cmd_bounds = [10, 10, 250] #[min_cmd, cmd_step, max_cmd]
volt_range = [14.4,0.2,15.2] #[min input_voltage, imput_voltage step, max input_voltage]
total_data = np.zeros(12)

for volt in np.arange(volt_range[0],volt_range[2]+volt_range[1],volt_range[1]):
	forcedata = analysis(volt,cmd_bounds)
	total_data = np.r_['0,2',total_data,forcedata]

total_data = np.delete(total_data,(0),axis=0)
np.save(path+'total_data',total_data)
np.savetxt(path+'total_data.txt',total_data,delimiter = '\t')

#B: [inputVoltage, command, averageForce]
B = np.zeros(3)
for volt in np.arange(volt_range[0],volt_range[2]+volt_range[1],volt_range[1]):
	volt_matrix = total_data[total_data[:,11] == volt]
	for cmd in range(cmd_bounds[0],cmd_bounds[2]+cmd_bounds[1],cmd_bounds[1]):
		cmd_matrix = volt_matrix[volt_matrix[:,0] == cmd]
		avgForce = np.mean(cmd_matrix[:,10])
		B = np.r_['0,2',B,[volt,cmd,avgForce]]
B = np.delete(B,(0),axis=0)
np.save(path+'matrix_B',B)
np.savetxt(path+'matrix_B.txt',B,delimiter = '\t')

#C: [ESC voltage, command, average force]
C = np.zeros(3)
for voltage in np.arange(14,15.4,0.1): #input values for range of ESC voltage reading
	if any(abs(voltage - total_data[:,6])<0.01):
		volt_matrix = total_data[abs(total_data[:,6] - voltage)<0.01]
		for cmd in range(cmd_bounds[0],cmd_bounds[2]+cmd_bounds[1],cmd_bounds[1]):
			if any(abs(cmd - volt_matrix[:,0])<0.01):
				cmd_matrix = volt_matrix[abs(volt_matrix[:,0]-cmd)<0.01]
				avgForce = np.mean(cmd_matrix[:,10])
				C = np.r_['0,2',C,[voltage,cmd,avgForce]]
C = np.delete(C,(0),axis=0)
np.save(path+'matrix_C',C)
np.savetxt(path+'matrix_C.txt',C,delimiter = '\t')

#D: [input voltage, command, average esc voltage]
D = np.zeros(3)
for volt in np.arange(volt_range[0],volt_range[2]+volt_range[1],volt_range[1]):
	volt_matrix0 = total_data[total_data[:,11] == volt]
	for cmd in range(cmd_bounds[0],cmd_bounds[2]+cmd_bounds[1],cmd_bounds[1]):
		cmd_matrix0 = volt_matrix0[volt_matrix0[:,0] == cmd]
		avgVolt = np.mean(cmd_matrix0[:,6])
		D = np.r_['0,2',D,[volt,cmd,avgVolt]]
D = np.delete(D,(0),axis=0)
np.save(path+'matrix_D',D)
np.savetxt(path+'matrix_D.txt',D,delimiter = '\t')
print ('Done')
