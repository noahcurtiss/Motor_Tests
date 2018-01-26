import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def escvolt_filter(A,escvolt):
	voltMatrix = np.zeros(12)
	for line in A:
		if (round(line[6],1) == escvolt):
			voltMatrix = np.vstack((voltMatrix,line))
	voltMatrix = np.delete(voltMatrix,(0),axis=0)
	return voltMatrix

total_data = np.load('/home/noah/Documents/total_data.npy')

voltage_values = [10.6,11.3,12.0,12.6]

plt.figure(1)
plotnum = 221

inputforce = 3
inputvolt = 11.7
i = 0
cmddata = np.zeros(4)

for volt in voltage_values:
	voltdata = escvolt_filter(total_data,volt)

	force = voltdata[:,10]
	cmd = voltdata[:,0]

	fit = np.polyfit(force,cmd,2)
	f = np.poly1d(fit)

	cmddata[i] = f(inputforce)
	i+=1

	force_new = np.linspace(0,8,num=1000)
	cmd_new = f(force_new)

	plt.subplot(plotnum)
	plt.plot(force,cmd,'o', force_new, cmd_new)
	plotnum += 1

fitout = np.polyfit(voltage_values,cmddata,2)
fout = np.poly1d(fitout)

plt.figure(2)
volt_new = np.linspace(10.5,12.7,num=1000)
cmd_new = fout(volt_new)

plt.plot(voltage_values,cmddata,'o', volt_new, cmd_new)

cmdout = fout(inputvolt)
print cmdout
plt.show()