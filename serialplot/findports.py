#! python3

import sys
import glob
import serial
from serial import SerialException

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
	
if __name__=='__main__':
	print(serial_port())
	port_list=serial_port()
	port1=port_list[0]
	port1=''.join(port1)
	ser1=serial.Serial(port1, 38400)
	port2=port_list[1]
	port2=''.join(port2)
	ser2=serial.Serial(port2, 38400)
	print(port1+' '+port2)