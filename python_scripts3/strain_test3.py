import numpy as np
import matplotlib.pyplot as plt


total_data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/robbe/total_data.txt')

avg_matrix = np.array([0])

# i=0
# for i in range(50,np.size(strain_data),1):
# 	avg = np.mean(strain_data[0:i])
# 	avg_matrix = np.append(avg_matrix,avg)

plt.figure(1)
plt.plot(total_data[:500,7])
#plt.xlabel('time')
#plt.ylabel('strain gauge reading')
#plt.title('Strain Readings During Startup')
plt.grid()
plt.show()

#print(np.mean(loading[0:600,0]),np.mean(unloading[600:,0]),np.mean(loading[1100:,0]),np.mean(unloading[0:150,0]))