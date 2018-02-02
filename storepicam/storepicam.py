#! python3

from time import sleep
import picamera
from datetime import datetime
import sys
import glob
import serial
from serial import SerialException
import numpy as np
from time import time
from datetime import datetime

def serial_port():	#get avalable ports
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
port=port_list[0]
port=''.join(port)
ser=serial.Serial(port, 38400)

picdir='/home/pi/datalog/picamlog/'
datadir='/home/pi/datalog/lampirdata/'

camera=picamera.PiCamera()
camera.resolution=(960,720)

ser.flushInput()
filename=datetime.now().strftime("%Y-%m-%d %H-%M-%S")
outfile=datadir+filename+'.csv'

camfile=picdir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.jpg'
camera.capture(camfile)

pic_start=datetime.now()
data_start=datetime.now()

while True:
	pic_dt=datetime.now()-pic_start
	data_dt=datetime.now()-data_start
	f=open(outfile,'a')
	if pic_dt.seconds<=15 and data_dt.seconds<=60:
		data=ser.readline()
		f.write(str(data))
		f.write(str(datetime.now()))
		f.write('\n')
	elif pic_dt.seconds>15 and data_dt.seconds<=60:
			print('new pic')
			pic_start=datetime.now()
			camfile=picdir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.jpg'
			camera.capture(camfile)
			data=ser.readline()
			f.write(str(data))
			f.write(str(datetime.now()))
			f.write('\n')
	elif pic_dt.seconds<=15 and data_dt.seconds>60:
			f.close()
			print('new file')
			data_start=datetime.now()
			filename=datetime.now().strftime("%Y-%m-%d %H-%M-%S")
			outfile='/home/pi/datalog/lampirdata/'+filename+'.csv'
	else:
			print('new pic')
			pic_start=datetime.now()
			camfile=picdir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.jpg'
			camera.capture(camfile)
			f.close()
			print('new file')
			data_start=datetime.now()
			filename=datetime.now().strftime("%Y-%m-%d %H-%M-%S")
			outfile='/home/pi/datalog/lampirdata/'+filename+'.csv'

f.close()
	
# close serial
ser.flush()
ser.close()
