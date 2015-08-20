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
	temp_data = ser.readline().split(',')
	print(temp_data[1])
	return "the temperature is " + temp_data[1].split('.')[0] + " C"

def get_humidity_string():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"s")
	temp_data = ser.readline().split(',')
	print(temp_data[0])
	return "the humidity is at " + temp_data[0].split('.')[0] + "%"

def give_treat_and_thank():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"t")
	print(ser.readline())
	time.sleep(3)
	return "thanks! I love treats :D"


serial_path = "/dev/ttyUSB0"

# open file with access keys and tokens
f = open("/home/pi/IsMartinRunning/.secrets/ORTHRUS.access")

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
	f = open("/home/pi/IsMartinRunning/get_mentions/most_recent")
	most_recent = f.read().strip()
	f.close()

	# compare current id to most recent
	if str(mention["id"]) == most_recent:
		new = False

	# skip it
	if not new:
		continue

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
		else:
			reply_string += " :)"


	if reply_string:
		reply = "@" + mention["user"]["screen_name"] + " " + reply_string
		print(">>>>>>  " + reply)
		twitter.update_status(status=reply)
	
	print("\n")

# save new most recently responded to id
f = open("/home/pi/IsMartinRunning/get_mentions/most_recent", "w")
f.write(replacement_most_recent)
f.close()

