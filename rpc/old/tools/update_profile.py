#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient
from onename_register import update_name
import os 

MONGODB_URI = os.environ['MONGODB_URI']
HEROKU_APP = os.environ['HEROKU_APP'] 
remote_client = MongoClient(MONGODB_URI)
users = remote_client[HEROKU_APP].user

#-----------------------------------
def update_profile(username,profile):
 
	onename_username = 'u/' + username

	print onename_username
	print json.dumps(profile)
	
	#update_name does json.dumps internally
	update_name(onename_username,profile)

#-----------------------------------
def update_profile_from_DB(username):

	entry = users.find_one({'username':username})
	profile = json.loads(entry['profile'])

	update_profile(username,profile)

#-----------------------------------
def update_profile_from_file(username,file_name='tools/json_profile.json'):

	json_data=open(file_name)
	profile = json.load(json_data)

	update_profile(username,profile)

#-----------------------------------
if __name__ == '__main__':

	username = 'gavin'
	#update_profile_from_DB(username)
	update_profile_from_file(username)
