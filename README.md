# README #


### This project consists several parts:###
 * LAMPIR driven code, based on arduino
 * Raspberry Pi code for camera, data storage
 * Human detection of photos and analog data analyzing


### How do I get set up? ###
1. LAMPIR is as a slave of Raspi. it runs arduino continuously. 
2. Raspi runs python code, with multithread to collect data (plot) and storage photos. See (https://www.tutorialspoint.com/python/python_multithreading.htm)
3. Filename is based on the time.
4. Picamera takes record video continously, the video files are seperated by 1 min.
5. (2/21/18) The current running code is ./videolog/videolog.py.
   
### How to use code to synchronized log video and PIR output ###
1. The code must run under raspberry PI3. PiCam must present as well as LAMPIR node.
2. Final code is in ./videolog/videolog.py
3. Afterrunning, the video and analog output will be stored in 'videodir='/home/pi/datalog/videolog/'' and 'datadir='/home/pi/datalog/lampirdata/'', with 1 min intervals. 

### Contribution guidelines ###



copyright by Libo Wu