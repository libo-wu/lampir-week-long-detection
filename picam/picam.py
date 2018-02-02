#! python3

from time import sleep
import picamera
from datetime import datetime

storedir='/home/pi/datalog/picamlog/'

camera=picamera.PiCamera()
camera.resolution=(960,720)

camfile=storedir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.jpg'
camera.capture(camfile)

start_time=datetime.now()

while True:
    dt=datetime.now()-start_time
    if dt.seconds<=10:
        pass
    else:
        print('new pic')
        start_time=datetime.now()
        camfile=storedir+datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.jpg'
        camera.capture(camfile)