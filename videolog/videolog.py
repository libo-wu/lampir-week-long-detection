#! python3

from time import sleep
import picamera
from datetime import datetime
import sys
import glob
import serial
from serial import SerialException
#import numpy as np
from time import time
import time
from datetime import datetime
import threading
from threading import Thread


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

class videolog(Thread):
    def run(self):
        while True:
            videoname=videodir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.h264'
            camera.start_recording(videoname)
            camera.wait_recording(60)
            camera.stop_recording()
            print('video complete: '+datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

class datalog(Thread):
    def run(self):
        while True:
            data_start=datetime.now()
            filename=datadir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.csv'
            f=open(filename,'a')
            while (datetime.now()-data_start).seconds<=60:
                data=ser.readline()
                f.write(str(data))
                f.write(str(datetime.now()))
                f.write('\n')
            f.close()
            print('data complete: '+datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
	
	
port_list=serial_port()
port=port_list[0]
port=''.join(port)
ser=serial.Serial(port, 38400)

videodir='/home/pi/datalog/videolog/'
datadir='/home/pi/datalog/lampirdata/'

camera = picamera.PiCamera()
camera.resolution = (640, 480)

if __name__=='__main__':
    a=videolog()
    b=datalog()
    a.start()
    b.start()