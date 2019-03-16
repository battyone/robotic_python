# import the necessary packages
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from random import *
import RPi.GPIO as GPIO
import time
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib #for reading image from URL
 
# Motor setup 
PWM_DRIVE_LEFT = 21		# ENA - H-Bridge enable pin
FORWARD_LEFT_PIN = 26	# IN1 - Forward Drive
REVERSE_LEFT_PIN = 19	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5		# ENB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 13	# IN1 - Forward Drive
REVERSE_RIGHT_PIN = 6	# IN2 - Reverse Drive
 
# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)
 
# Initialise objects for H-Bridge digital GPIO pins
forwardLeft = DigitalOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = DigitalOutputDevice(REVERSE_LEFT_PIN)
forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)

def computerchoice(number):  # Turn on the leb to show what computer choice
    GPIO.output(number,GPIO.HIGH)

def turnledoff():    # turn all led off
    GPIO.output(17,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)
    GPIO.output(27,GPIO.LOW)

def allStop():     # stop all motor
	forwardLeft.value = False
	reverseLeft.value = False
	forwardRight.value = False
	reverseRight.value = False
	driveLeft.value = 0
	driveRight.value = 0
 
def forwardDrive():   # set motor run forward
	forwardLeft.value = True
	reverseLeft.value = False
	forwardRight.value = True
	reverseRight.value = False
	driveLeft.value = 1.0
	driveRight.value = 1.0
 

# status ready to play
play = 0
status = 0
human = 0
computer = 0
com = 0

# setup led GPIO 22,27,17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'orange':(20,255,255)}
 
# define standard colors for circle around the object
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'orange':(0,140,255)}
 
#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
   
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
       
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
       
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                # cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                # print(key ) 
                if computer <=5 and human <=5:
                    if key in ['orange'] :    # status ready
                        if status != 1 :
                            if com == 1:
                                forwardDrive()
                                time.sleep(3)
                                allStop()
                                com = 0
                            print("ready to play")   # ready to play
                            turnledoff()
                        status = 1
                    elif key in ['blue']:  # status "la" -- パー 1  -- GPIO 17
                        x = randint(1, 3)
                        if status != 2 :
                            # print("blue")
                            if x == 3:    # computer vs human :  チョキ vs パー 
                                print("computer vs human :  チョキ vs パー ")
                                print("computer win")
                                computerchoice(27)
                                computer +=1
                                com = 1
                            if x == 2:    # computer vs human :  グ－ vs パー
                                print("computer vs human :  グ－ vs パー")
                                print("human win")
                                computerchoice(22)
                                human +=1
                            if x == 1:
                                print("computer vs human :  パー vs パー")
                                computerchoice(17)
                        status = 2
                    elif key in ['red']:  # status "dam" -- グ－ 2  -- GPIO 22
                        x = randint(1, 3)
                        if status != 3:
                            # print ("red")
                            if x == 1:   # computer vs human : パー vs グ－
                                print("computer vs human : パー vs グ－")
                                print("computer win")
                                computerchoice(17)
                                computer +=1
                                com = 1
                            if x == 3:   # computer vs human : チョキ vs グ－
                                print("computer vs human : チョキ vs グ－")
                                print("human win")
                                computerchoice(27)
                                human +=1
                            if x == 2:
                                print("computer vs human : グ－ vs グ－")
                                computerchoice(22)
                        status = 3
                    else:                  # status "keo" -- チョキ 3   --GPIO 27
                        x = randint(1, 3)
                        if status !=4:
                            # print ("green")
                            if x == 1:   # computer vs human : パー vs チョキ
                                print("computer vs human : パー vs チョキ")
                                print("human win")
                                computerchoice(17)
                                human +=1
                            if x == 2:   # computer vs human : グ－ vs チョキ
                                print("computer vs human : グ－ vs チョキ")
                                print("computer win")
                                computerchoice(22)
                                com = 1
                                computer +=1
                            if x == 3:
                                print("computer vs human : チョキ vs チョキ")
                                computerchoice(27)
                        status = 4
                if computer == 5:
                    print("computer winnnnnnnnnn")
                    turnledoff()
                    computer += 1
                if human == 5:
                    print("congratulate human")
                    turnledoff()
                    human += 1   
                # cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
 
     
    # show the frame to our screen
    cv2.imshow("Frame", frame)
   
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()