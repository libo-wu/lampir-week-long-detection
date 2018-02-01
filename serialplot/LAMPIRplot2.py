import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
import sys
import glob
from time import time


def serial_port(): # list ports
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
	
port_list=serial_port() # noramlly, arduino has port name 'ttyUSB01...'
port=port_list[0]
port=''.join(port)
ser=serial.Serial(port, 38400)

voltage=[]

plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0

def makeFig(): #Create a function that makes our desired plot
    plt.ylim(-0.1, 5.1)                                 #Set y min and max values
    plt.title('LAMPIR voltage')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Voltage/V')                            #Set ylabels
    plt.plot(voltage,'r-',label='voltage')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    
ser.flushInput()
run=True

while run: # While loop that loops forever
	try:
		arduinodata=ser.readline()
		ydata=arduinodata
		voltage.append(float(ydata)*5.0/1024)
		before=time()
		drawnow(makeFig)
		print(time()-before)
		plt.pause(0.000001)
		cnt=cnt+1
		if(cnt>200):
			voltage.pop(0)
	except KeyboardInterrupt:
		print ('q')
		run=False
		break


# close serial
ser.flush()
ser.close()
