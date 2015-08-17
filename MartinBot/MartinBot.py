#!/usr/bin/env python
import sys
import pygame
import pygame.camera
import os
from twython import Twython
from pygame.locals import *

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
image = cam.get_image()
pygame.image.save(image,'/home/pi/MartinBot/image.jpg')

#os.system("fswebcam -d /dev/video0 --no-banner /home/pi/MartinBot/image.jpg")

# get args from listening to arduino
running_data = sys.argv[1].split(',')

# generate tweet text
message = "Just ran " + running_data[4] + "m! #crossfit #NotACult"

# open file with access keys and tokens
f = open("/home/pi/.secrets/martinBot.access")

# assign keys and tokens
secrets = f.read().split("\n")

# sort them
apiKey = secrets[0]
apiSecret = secrets[1]
accessToken = secrets[2]
accessTokenSecret = secrets[3]

# instantiate Twython
api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

photo = open('image.jpg','rb')
api.update_status_with_media(media=photo, status=message)

print("all good")

