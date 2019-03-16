# gPBL_2019 
#Hanoi University of Science and Technology - Shibaura Institute of Technology

# Active Flow

![demo](https://github.com/vinhyenvodoi98/robotic_python/blob/master/picture/demo.jpg)


Play Rock paper scissors with robot by color. Blue is paper, Green is scissors, Red is Rock. We show what color we choice with camera . Game will start and computer show what computer choice by turn on the led .

![mechanism](https://github.com/vinhyenvodoi98/robotic_python/blob/master/picture/mechanism.png)

**This project using** 
* Raspberry Pi3 + camera
* Motor driver tb6612FNG
* Led and some electronic parts

**Install**
* python3 > 3.5 , pip3
* cv2,numpy

# About file

**detectcolor_leccontrol_motorcontrol.py** is complite code . It can detect color , choice rundom number and show what computer choice by using led . If computer win computer's car will run . If human win human's car will run . Who win 5 time is truly winner

**motor-driver.py** we using this code for test motor driver tb6612FNG 

**led-control.py** we using this code for turn on and turn off the led 

# Open source
Detect color : 
    https://pastebin.com/WVhfmphS

motor driver tb6612FNG:
    https://www.bluetin.io/dc-motors/motor-driver-raspberry-pi-tb6612fng/
