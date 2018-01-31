

import sys
import glob
import serial
from serial import SerialException
import numpy as np
from matplotlib import pyplot as plt
from time import time

def serial_port():
	'''list port names'''

	if sys.platform.startswith('win'):
		ports=['COM%s' % (i+1)for i in range (256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		ports=glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports=glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')
		
	result=[]
	for port in ports:
		try:
			s=serial.Serial(port)
			s.close()
			result.append(port)
		except(OSError, serial.SerialException):
			pass
	return result
	
port_list=serial_port()
port=''.join(port_list)
ser=serial.Serial(port, 38400)

plt.ion()

start_time=time()
timepoints=[]
ydata=[]
yrange=[-0.1, 5.1]
view_time =20 #seconds of data to  view at once
duration = 60 # total seconds to collect data

fig1=plt.figure()
fig1.suptitle('LAMPIR voltage', fontsize='18', fontweight='bold')
plt.xlabel('time')
plt.ylabel('voltage')
plt.axes().grid(True)
line1, = plt.plot(ydata)
plt.ylim(yrange)
plt.xlim([0,view_time])

ser.flushInput()

run=True

while run:
	ser.reset_input_buffer()
	data=ser.readline()
	
	try:
		ydata.append(float(data)*5.0/1024)
		timepoints.append(time()-start_time)
		current_time=timepoints[-1]
		
		line1.set_xdata(timepoints)
		lin1.set_ydata(ydata)
		
		# slide the xaxis
		if current_time>view_time:
			plt.xlim([current_time-view_time, current_time])
		
		#when time is up, kill the plot and collect loop
		if timepoints[-1]>duration: run=False
		
	except: pass
	
	fig1.canvas.draw()
	
ser.close()
















