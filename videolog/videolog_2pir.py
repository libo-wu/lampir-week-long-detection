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
                data=ser1.readline()
                f.write(str(data))
                f.write(str(datetime.now()))
                f.write('\n')
            f.close()
            print('lampir data complete: '+datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
	
class pirlog(Thread):
    def run(self):
        while True:
            pirdata_start=datetime.now()
            pirfilename=pirdir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'-pir'+'.csv'
            f1=open(pirfilename,'a')
            while (datetime.now()-pirdata_start).seconds<=60:
                pirdata=ser2.readline()
                f1.write(str(pirdata))
                f1.write(str(datetime.now()))
                f1.write('\n')
            f1.close()
            print('pir data complete: '+datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

port_list=serial_port()
port1=port_list[0]    #port1 is usb1, uppper port, lampir
port1=''.join(port1)
ser1=serial.Serial(port1, 38400)

port2=port_list[1]    #port2 is usb0, bottom port, pir
port2=''.join(port2)
ser2=serial.Serial(port2, 38400)

videodir='/home/pi/datalog/videolog/'
datadir='/home/pi/datalog/lampirdata/'
pirdir='/home/pi/datalog/pirdata/'

camera = picamera.PiCamera()
camera.resolution = (640, 480)

if __name__=='__main__':
    a=videolog()
    b=datalog()
    c=pirlog()
    a.start()
    b.start()
    c.start()