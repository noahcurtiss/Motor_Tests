import numpy as np
from scipy.interpolate import griddata
import math
import string

C = np.load('/home/noah/Documents/matrix_C.npy')

X = C[:,0]
Y = C[:,2]
Z = C[:,1]

points = np.c_[X,Y]

i=0
j=0

matrix = np.zeros((3,3))
for volt in np.arange(10.3,12.7,0.1):
	for force in np.arange(0,2,0.05):
		command = int(griddata(points, Z, (volt, force), method='linear'))
		matrix[i][j] = command
		j+=1
	i+=1
np.save('/home/noah/Documents/matrix',matrix)
np.savetxt('/home/noah/Documents/matrix.txt',matrix,delimiter = '\t')