# Running a Motor Test
1) Attach the motor to the test rig as shown in test_rig_setup.jpg. Measure the distance between the pivot and motor (b) and the pivot and sensor (d), preferably using calipers.

2) Connect the arduino to the force sensor and the ESC using the following connections:  
   **ESC <---> Arduino**  
   C <---> A5  
   D <---> A4  
   Gnd <---> Gnd 

   **Sensor <---> Arduino**  
   10 <---> A0  
   12 <---> Gnd  

3) Set up the force sensor.  
   _NOTE: The force sensor may need a few minutes to warm up. Values may start higher or lower than expected but will normalize after several minutes._

4) Run a force calibration:
    1. Upload strain_reader.ino to the arduino.
    2. With no weight on the sensor aside from the rig, run record.py for several seconds to determine the reading with zero thrust. Be sure to edit record.py with a suitable text file name and the port name corresponding to the arduino. A recommended text file name is '<motor><voltage>v1.txt'.
    3. Add a known mass to the rig and run record.py again. A recommended file name is '<motor><voltage>v2.txt'. You should now have two text files that contain a single column of data read from the force sensor.

5) Attach a power supply to the motor and set it at a specific voltage, checking with a multimeter. Voltage may drift during the tests so be prepared to adjust the supply accordingly.

6) Upload step_test.ino and run record.py (remember to update the file name). This should take about 15 mins.

7) Repeat steps 4-6 for each voltage you want to test. Let the motor cool between each test to keep the data consistent. It is important to do a force calibration before or after every test as the force sensor's readings could change.

8) Run analysis.py to filter data and format it for graphing. Be sure to update the file paths and tailor the data analysis to fit your own needs.

# Using the Motor Data
Using the data from analysis.py, you can run escVolt2cmd.py, escVolt2cmd_send.py, inputVolt2cmd.py, or inputVolt2cmd_send.py. Before running either of the send programs, do a force calibration, input the v1, v2, d, b, and m values into cmd_reader.ino, and then upload cmd_reader to the arduino. 
- inputVolt2cmd.py calculates the proper command given a desired force and input voltage
- inputVolt2cmd_send.py does the calculations of inputVolt2cmd.py and sends the command to the ESC.
- escVolt2cmd_send.py reads voltage from the esc, takes a desired force and calculates the proper command. It continuously updates the command based on the changing voltage.
- escVot2cmd.py simulates the behavior of escVolt2cmd_send.py by predicting the voltage change from a command change.

Data from the following motors is included:
- robbe Roxxy BL-Motor 2827-35, 760kv. 10x4.5 prop
- tiger mn3110-17, 700kv. 10x4.7 prop

