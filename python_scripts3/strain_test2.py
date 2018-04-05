import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


loading = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/loading.txt')
unloading = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/unloading.txt')
startup = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/startup.txt')
loaded = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/loaded.txt')

avg_matrix = np.array([0])

# i=0
# for i in range(50,np.size(strain_data),1):
# 	avg = np.mean(strain_data[0:i])
# 	avg_matrix = np.append(avg_matrix,avg)

# plt.figure(1)
# plt.plot(loading[600:1100,1],loading[600:1100,0])
# plt.xlabel('time')
# plt.ylabel('strain gauge reading')
# plt.title('Strain Readings During Loading')
# plt.grid()

# plt.figure(2)
# plt.plot(unloading[150:600,1],unloading[150:600,0])
# plt.xlabel('time')
# plt.ylabel('strain gauge reading')
# plt.title('Strain Readings During Unloading')
# plt.grid()
# plt.show()

# plt.figure(3)
# plt.scatter(startup[10000:,1],startup[10000:,0],marker='.')
# plt.xlabel('time')
# plt.ylabel('strain gauge reading')
# plt.title('Strain Readings After Startup')
# plt.grid()
# plt.show()

# plt.hist(startup[10000:20000,0],bins='auto')
# plt.show()

plt.figure(4)
plt.scatter(loaded[:,1],loaded[:,0],marker='.')
plt.xlabel('time')
plt.ylabel('strain gauge reading')
plt.title('Strain Readings Under Uniform Load')
plt.grid()
plt.show()

print(np.mean(startup[10000:20000,0]),np.median(startup[10000:20000,0]),np.mean(startup[10000:20000,0]))


print(np.mean(loading[0:600,0]),np.mean(unloading[600:,0]),np.mean(loading[1100:,0]),np.mean(unloading[0:150,0]))