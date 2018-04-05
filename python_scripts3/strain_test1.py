import numpy as np
import matplotlib.pyplot as plt


strain_data1 = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/strain_test1.txt')
strain_data2 = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/strain_test2.txt')
strain_data3 = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/strain_test3.txt')
strain_data4 = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/strain_test4.txt')
strain_data5 = np.loadtxt('/home/mbshbn/Documents/Motor_Tests/strain_tests/strain_test5.txt')

strain_data5 = strain_data5[500:]

strain_data = np.concatenate([strain_data1,strain_data3,strain_data5])

print(np.mean(strain_data1),np.mean(strain_data3),np.mean(strain_data5))

avg_matrix = np.array([0])

i=0
for i in range(50,np.size(strain_data),1):
	avg = np.mean(strain_data[0:i])
	avg_matrix = np.append(avg_matrix,avg)


plt.plot(avg_matrix)
plt.xlabel('count')
plt.ylabel('strain gauge reading')
plt.title('Strain Readings from Large Applied Load')
plt.grid()
plt.show()