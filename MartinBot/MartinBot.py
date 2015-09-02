#!/usr/bin/env python

# This Python script is triggered by wheel_listsner.sh.
# 
# It takes a photo using the webcam and tweets it with the data from the run
# usng the Twython library.
# 
# Remeber that if you're pi's username is not 'pi', or if you create this
# project somewhere different, the file paths will all need to change.
# 

# import libraries
import sys
import pygame
import pygame.camera
import os
from twython import Twython
from pygame.locals import *

# initialise the webcam and take a photo
pygame.init()
pygame.camera.init()
# you'll need to make sure this is refering to the right usb device (i.e. "/dev/video0")
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
image = cam.get_image()
pygame.image.save(image,'/home/pi/IsMartinRunning/MartinBot/image.jpg')

# get args from wheel_listener.sh
running_data = sys.argv[1].split(',')

# create data variables
time_checks = running_data[0]
total_time = str(float(running_data[1]) / 1000)
average_rotation_time = running_data[2]
speed = running_data[3]
distance = running_data[4]

# get personal bests
f = open("/home/pi/IsMartinRunning/MartinBot/personal_bests")
bests = f.read().split("\n")
best_speed = bests[0]
best_distance = bests[1]
f.close()

# generate tweet text
message = "Just ran " + distance + "m in " + total_time + " seconds!"

# check if personal best have been beaten
if (speed > best_speed) or (distance > best_distance):
	if (speed > best_speed) and (distance > best_distance):
		message += " That's new speed and distance records! #doublewhammy"
	else:
		if speed > best_speed:
			message += " That's the fastest I've ever run!!! #personalbest"
		if distance > best_distance:
			message += " I've never run that far before :D #personalbest"

	# replace personal bests with new ones
	f = open("/home/pi/IsMartinRunning/MartinBot/personal_bests", "w")
	f.write(speed + "\n" + distance)
	f.close()

# open file with access keys and tokens
f = open("/home/pi/IsMartinRunning/.secrets/martinBot.access")

# assign keys and tokens
secrets = f.read().split("\n")

# close the file
f.close()

# create access variables
apiKey = secrets[0]
apiSecret = secrets[1]
accessToken = secrets[2]
accessTokenSecret = secrets[3]

# instantiate Twython
api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

# tweet pic and message
print(message)
photo = open('image.jpg','rb')
api.update_status_with_media(media=photo, status=message)

print("all good")
