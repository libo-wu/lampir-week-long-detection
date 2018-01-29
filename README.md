# README #


### This project consists several parts:###
 * LAMPIR driven code, based on arduino
 * Raspberry Pi code for camera, data storage
 * Human detection of photos and analog data analyzing


### How do I get set up? ###
1. LAMPIR is as a slave of Raspi. it runs arduino continuously. 
2. Raspi runs python code, with multithread to collect data (plot) and storage photos.
3. Filename is based on the time.
4. Picamera takes photos every 1 min, or when triggerred.
   * When the analog signal exceeds a value, take photos.


### Contribution guidelines ###



copyright by Libo Wu