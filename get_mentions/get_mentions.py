#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This python script is run by the mention_listener.sh script.
# 
# It checks Twitter to see if anyone has tweeted at Martin and creates 
# an appropriate response.
# 
# It controls the temperature-humidity sensor as well as the servo
# for the treat dispenser.
# 
# Remeber that if you're pi's username is not 'pi', or if you create this
# project somewhere different, the file paths will all need to change.
# 

# import libraries
import sys
from twython import Twython
import pprint
import json
import re
import serial
import time


# function to generate a temperature response
def get_temp_string():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"s")
	temp_data = ser.readline().split(',')
	print(temp_data[1])
	return "the temperature is " + temp_data[1].split('.')[0] + " C"

# funciton to generate a humididty response
def get_humidity_string():
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"s")
	temp_data = ser.readline().split(',')
	print(temp_data[0])
	return "the humidity is at " + temp_data[0].split('.')[0] + "%"

# function to activate the treat dispenser and generate a thank you response
def give_treat_and_thank():
	# send data to the arduino
	ser = serial.Serial(serial_path, 9600)
	ser.write(b"t")
	# make sure you get a response
	print(ser.readline())
	# wait a bit
	time.sleep(3)
	return "thanks! I love treats :D"

# this is the path for the temperature/treat dispenser arduino
# yours may be different (e.g. /dev/ttyACM0)
serial_path = "/dev/ttyUSB0"

# open file with access keys and tokens
f = open("/home/pi/IsMartinRunning/.secrets/mentions.access")

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

# get info about recent mentions
data = twitter.get_mentions_timeline(count=10)

# useful variables
new = True
first = True
replacement_most_recent = ""

# look at each mention
for mention in data:

	# if top of the list, save id (this wil be the new most recently responded to)
	if first:
		replacement_most_recent = str(mention["id"])
		first = False

	# get id of previous most recent tweet responded to
	f = open("/home/pi/IsMartinRunning/get_mentions/most_recent")
	most_recent = f.read().strip()
	f.close()

	# compare current id to most recent
	if str(mention["id"]) == most_recent:
		new = False

	if not new:
		# skip it
		continue

	# output some data about the mention to the console
	print(mention["user"]["name"] + " (" + mention["user"]["screen_name"] + ")" + ":")
	print("\t" + mention["text"])

	# make the mention text lower case
	text = mention["text"].lower()

	reply_string = ""

	keywords = ["hot", "cold", "temperature", "humidity", "weather", "treat"]

	# check if any keywords are in the mention text
	if any(s in text for s in keywords):

		# use response generation functions
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
		# output what we are tweeting to the console
		reply = "@" + mention["user"]["screen_name"] + " " + reply_string
		print(">>>>>>  " + reply)
		# send the tweet
		twitter.update_status(status=reply)
	
	print("\n")

# save new most recently responded to id
f = open("/home/pi/IsMartinRunning/get_mentions/most_recent", "w")
f.write(replacement_most_recent)
f.close()
