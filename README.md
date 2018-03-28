# README #


### This project consists several parts: ###
 * LAMPIR driven code, based on arduino
 * Raspberry Pi code for camera, data storage
 * Human detection of photos and analog data analyzing


### How do I get set up? ###
1. LAMPIR and PIR are as slaves of Raspi.
2. Raspi runs Python code, with multithread to collect data (plot) and storage photos. See [Python multithreading](https://www.tutorialspoint.com/python/python_multithreading.htm).
3. Filename is the system time when starting recording.
4. Picamera takes record video continously, the video files are seperated by 1 min.
   
### How to use code to synchronized log video and PIR output ###
1. The code <b>MUST</b> run under raspberry PI3. PiCam must present as well as LAMPIR node.
2. Final code is in `./videolog/videolog.py` or `./videolog/videolog_2pir.py` (for logging data from LAMPIR and traditional PIR).
3. Afterrunning, the video and analog output will be stored in `videodir='/home/pi/datalog/videolog/'`, `datadir='/home/pi/datalog/lampirdata/'` `pirdir='/home/pi/datalog/pirdata`, with 1 min intervals. 

### Dataprocess of voltage signals ###
1. All analog signals are converted through an ADC on Arduino board, range from (0, 1024), indicating (0, 5 V). Raspi logs these data into a `.CSV` file, in such form: `b'526\n'2018-03-08 17:57:40.330576`.
2. A preprocessing is required to extract such signals as well as meaningful time stamps.
3. Types of data signals:

High frequency | Signal high Vpp | Single low Vpp  
---|---|---
Moving	| Stationary |	Unoccupied
4. First step is seperate high and low frequency.
5. Second step is classify stationay and unoccupied scenarios in low frequency signals.




copyright by Libo Wu, libo.wu@stonybrook.edu
