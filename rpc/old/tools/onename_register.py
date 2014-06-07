#!/usr/bin/env python
# -*- coding: utf-8 -*-

SLEEP_INTERVAL = 3

from time import sleep
import csv
import requests
import json

from coinrpc.coinrpc import namecoind_blocks, namecoind_name_new, check_registration, namecoind_name_update

from pymongo import Connection
conn = Connection()
db = conn['namecoin']
queue = db.queue
codes = db.codes
remoteusers = db.remoteusers

from pymongo import MongoClient
import os 

MONGODB_URI = os.environ['MONGODB_URI']
HEROKU_APP = os.environ['HEROKU_APP'] 
remote_client = MongoClient(MONGODB_URI)
users = remote_client[HEROKU_APP].user

#-----------------------------------
def utf8len(s):
	return len(s.encode('utf-8'))

#-----------------------------------
def save_name_new_info(info,key,value):
	reply = {}
  
	try:
		
		reply['longhex'] = info[0]
		reply['rand'] = info[1]
		reply['key'] = key
		reply['value'] = value
	
		#get current block...
		blocks = namecoind_blocks()

		reply['current_block'] = blocks['blocks']
		reply['wait_till_block'] = blocks['blocks'] + 12
		reply['activated'] = False
		
		#save this data to Mongodb...
		queue.insert(reply)

		reply['message'] = 'Your registration will be completed in roughly two hours'
		del reply['_id']        #reply[_id] is causing a json encode error
		
	except Exception as e:
		reply['message'] = "ERROR:" + str(e)
	
	return reply 

#-----------------------------------
def slice_profile(username, profile):

	#need u/ for OneName usernames
	key1 = 'u/' + username.lower()
	key2 = 'i/' + username.lower() + '-1'

	if utf8len(str(profile)) < 520:
		return key1, profile, None, None 

	value1 = {}
	value2 = {}

	first_keys = ['v', 'name', 'bitcoin', 'pgp', 'website', 'location', 'bio']

	for key in profile.keys():
		if(key in first_keys):
			value1[key] = profile[key]
		else:
			value2[key] = profile[key]
			
	#don't allow more than 519 bytes of data in the namecoin blockchain (their bug/limit)
	if utf8len(str(value1)) > 519 or utf8len(str(value2)) > 519:
		print "error: more than 519 bytes in value"
		raise RuntimeError

	if value2.keys() == []:
		return key1, value1, None, None 
	else:
		value1['next'] = key2
		return key1, value1, key2, value2 

#-----------------------------------
def register_name(key,value):

	info = namecoind_name_new(key,json.dumps(value))

	reply = save_name_new_info(info,key,json.dumps(value))
	
	print reply
	print '---'
	#sleep(SLEEP_INTERVAL)

#-----------------------------------
def update_name(key,value):

	reply = {}

	info = namecoind_name_update(key,json.dumps(value))

	reply['key'] = key
	reply['value'] = value
	reply['activated'] = True 

	#save this data to Mongodb...
	check = queue.find_one({'key':key})

	if check is None:
		queue.insert(reply)
	else:
		queue.save(reply)

	print reply
	print info
	print '---'
	#sleep(SLEEP_INTERVAL)

#-----------------------------------
def main_loop(username,profile,accesscode=None):

	key1, value1, key2, value2 = slice_profile(username,profile)

	reply = queue.find_one({'key':key1})

	if reply is None:
		#not in DB 
		print "not registered: " + key1

		if check_registration(key1):
			print "name reserved"
			code = codes.find_one({'username':key1})
			if code['accesscode'] == accesscode:
				print "code match"
				update_name(key1,value1)
				if key2 is not None:
					register_name(key2,value2)
		else:
			print "name new"
			register_name(key1,value1)
			if key2 is not None:
				register_name(key2,value2)


	#quick hack for key2 registration error
	'''
	if key2 is not None:
		if check_registration(key2):
			pass
		else: 
			register_name(key2,value2)
	'''

#-----------------------------------
def check_new_registrations():

	counter = 0

	print '-' * 5
	print "Checking for new users"
	for i in users.find():
		try:

			if i['dispatched'] is False:
				accesscode = None

				try:
					accesscode = i['accesscode']
				except:
					pass

				print i['username']
				#print i['accesscode']
				main_loop(i['username'],json.loads(i['profile']),accesscode)

				username = 'u/' + i['username'].lower()
				extended = 'i/' + i['username'].lower() + '-1'

				local = queue.find_one({'key':username})
				if local is not None:
					print "in local DB"
					i['dispatched'] = True
					remoteusers.insert(i)
					users.save(i)
				
				print '-' * 5
			else:
				counter += 1

		except Exception as e:
			pass

	print "Registered users: " + str(counter)

#-----------------------------------
if __name__ == '__main__':

	check_new_registrations()