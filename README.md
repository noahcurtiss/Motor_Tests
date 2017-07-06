# Running a Motor Test
1) Attach the motor to the test rig as shown below. Measure the distance between the fulcrum and motor and the fulcrum and sensor, preferably using calipers.

2) Connect the arduino to the force sensor and the i2c ESC using headers connecting the following ports:
	ESC <--> Arduino
	C   <--> A5
	D   <--> A4
	Gnd <--> Gnd

	Sensor <--> Arduino
	10     <--> A0
	12     <--> Gnd

3) Set up the force sensor. NOTE: The force sensor may need a few minutes to warm up. Values may start higher or lower than expected but will normalize after a several minutes.

4) Run a force calibration: Upload strain_reader.ino to the arduino. With no weight on the sensor aside from the rig, run record.py for several seconds to determine the reading with zero thrust. Be sure to edit record.py with a suitable rext file name and the port name corresponding to the arduino. A recommended text file name is '<motor><voltage>v1.txt'. Add a known mass to the rig and run record.py again. A recommended file name is '<motor><voltage>v2.txt'. You should now have two text files that contain a single column of data read from the force sensor.

5) Attach a power supply to the motor and set it at a specific voltage, checking with a multimeter. Voltage may drift during the tests so be prepared to adjust the supply accordingly.

6) Upload step_test.ino and run record.py (remember to update the file name). This should take about 15 mins.

7) Repeat steps 4-6 for each voltage you want to test. It is important to do a force calibration before or after every test as the force sensors' readings could change.

8) Run analysis.py. Be sure to update the file paths and tailor the data analysis to fit your own needs. For further analysis, Matlab files are also included.

