#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from twython import Twython
import pprint
import json
import re
import serial
import time


def get_temp_string():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"s")
	print(ser.readline())
	return "the temperature is hot"

def get_humidity_string():
	return "it's pretty humid"

def give_treat_and_thank():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"t")
	print(ser.readline())
	time.sleep(3)
	return "thanks! I love treats :D"


serial_path = "/dev/ttyUSB3"

# open file with access keys and tokens
f = open("/home/pi/.secrets/ORTHRUS.access")

# assign keys and tokens
secrets = f.read().split("\n")

# close the file
f.close()

# sort them
apiKey = secrets[0]
apiSecret = secrets[1]
accessToken = secrets[2]
accessTokenSecret = secrets[3]

# instantiate Twython
twitter = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

# do stuff:

# get info about recent mentions
data = twitter.get_mentions_timeline(count=10)

new = True
first = True
replacement_most_recent = ""

for mention in data:

	# if top of the list, save id
	if first:
		replacement_most_recent = str(mention["id"])
		first = False

	# get id of most recent tweet responded to
	f = open("/home/pi/get_mentions/most_recent")
	most_recent = f.read().strip()
	f.close()

	# compare current id to most recent
	if str(mention["id"]) == most_recent:
		new = False

	# skip it
#	if not new:
#		continue

	print(mention["user"]["name"] + " (" + mention["user"]["screen_name"] + ")" + ":")
	print("\t" + mention["text"])

	text = mention["text"].lower()

	reply_string = ""

	keywords = ["hot", "cold", "temperature", "humidity", "weather", "treat"]

	if any(s in text for s in keywords):

		if "weather" in text:
			reply_string += get_temp_string()
			reply_string += " and "
			reply_string += get_humidity_string()

		elif any(s in text for s in ["hot", "cold", "temperature"]):
			reply_string += get_temp_string()

		elif "humidity" in text:
			reply_string += get_humidity_string()

		if "treat" in text:
			reply_string += give_treat_and_thank()



	if reply_string:
		reply = "@" + mention["user"]["screen_name"] + " " + reply_string
		print(">>>>>>  " + reply)
		# twitter.update_status(status=reply)
	
	print("\n")

# save new most recently responded to id
f = open("/home/pi/get_mentions/most_recent", "w")
f.write(replacement_most_recent)
f.close()

