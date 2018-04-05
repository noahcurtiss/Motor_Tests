import numpy as np
import matplotlib.pyplot as plt

B = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/robbe/matrix_B.txt')

cmd = 200

if any(abs(cmd - B[:,1])<0.01):
	cmd_matrix = B[abs(B[:,1]-cmd)<0.01]

plt.plot(cmd_matrix[:,0],cmd_matrix[:,2])
plt.show()