import numpy as np
import matplotlib.pyplot as plt

v1 = np.loadtxt('14.2v1.txt')
v2 = np.loadtxt('14.2v2.txt')
v1_ = np.loadtxt('14.2v1_.txt')
v2_ = np.loadtxt('14.2v2_.txt')
v1__ = np.loadtxt('14.2v1__.txt')
v2__ = np.loadtxt('14.2v2__.txt')

data = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/tiger700/14.2.txt')
strain_data = np.loadtxt('saturation_test.txt')

v1m = np.mean(v1)
v2m = np.mean(v2)
v1_m = np.mean(v1_)
v2_m = np.mean(v2_)
v1__m = np.mean(v1__)
v2__m = np.mean(v2__)

plt.plot(data[:,7])
plt.xlabel('count')
plt.ylabel('strain gauge reading')
plt.title('Strain Readings Throughout a Motor Test')
plt.show()

# plt.plot(strain_data)
# plt.xlabel('count')
# plt.ylabel('strain gauge reading')
# plt.title('Strain Readings from Large Applied Load')
# plt.show()


print (v1m,v2m,v1_m,v2_m,v1__m,v2__m)