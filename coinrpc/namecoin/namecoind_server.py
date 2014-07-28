#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

VALUE_MAX_LIMIT = 520

import json
import namecoinrpc
from commontools import utf8len, error_reply

#---------------------------------------
class NamecoindServer(object):

	#-----------------------------------
	def __init__(self, server, port, user, passwd, use_https=True, passphrase=None):
		
		self.passphrase = passphrase
		self.server = server 

		self.namecoind = namecoinrpc.connect_to_remote(user, passwd, 
										host=server, port=port, 
										use_https=use_https)

	#-----------------------------------
	def blocks(self):
		reply = {}
		info = self.namecoind.getinfo()
		reply['blocks'] = info.blocks
		return reply


	#-----------------------------------
	#step-1 for registrering new names 
	def name_new(self, key,value):
		
		#check if this key already exists
		if self.check_registration(key):
			return error_reply("This key already exists")
			
		#check if passphrase is valid
		if not self.unlock_wallet(self.passphrase):
			return error_reply("Wallet passphrase is incorrect", 403)

		#create new name
		#returns a list of [longhex, rand]
		info = self.namecoind.name_new(key)
		
		return info


	#----------------------------------------------
	#step-2 for registering 
	def firstupdate(self, key,rand,value,tx=None):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Wallet passphrase is incorrect", 403)

		if tx is not None: 
			info = self.namecoind.name_firstupdate(key, rand, value, tx)
		else:
			info = self.namecoind.name_firstupdate(key, rand, value)

		return info

	#-----------------------------------
	def name_update(self, key,value):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#now unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Wallet passphrase is incorrect", 403)
			
		#update the 'value'
		info = self.namecoind.name_update(key, value)

		return info

	#-----------------------------------
	def transfer(self, key,new_address,value=None):
	 
		#check if this name exists and if it does, find the value field
		#note that update command needs an arg of <new value>.
		#in case we're simply transferring, we need to obtain old value first

		key_details = self.name_show(key)

		if 'code' in key_details and key_details.get('code') == -4:
			return error_reply("Key does not exist")

		#get new 'value' if given, otherwise use the old 'value'
		if value is None: 
			value = json.dumps(key_details['value'])

		#now unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Wallet passphrase is incorrect", 403)
		
		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#transfer the name (underlying call is still name_update)
		info = namecoind.name_update(key, value, new_address)

		return info

	#-----------------------------------
	def check_registration(self, key):

		info = self.namecoind.name_show(key)
		
		if 'code' in info and info.get('code') == -4:
			return False
		elif 'expired' in info and info.get('expired') == 1:
			return False
		else:
			return True

	#-----------------------------------
	def validate_address(self, address):

		reply = {}
		info = self.namecoind.validateaddress(address)
		
		info['server'] = self.server

		return json.dumps(info)

	#-----------------------------------
	def get_full_profile(self, key):

		check_profile = self.name_show(key)
		
		try:
			check_profile = check_profile['value']
		except:
			return check_profile
					
		if 'next' in check_profile:
			try:
				child_data = self.get_full_profile(check_profile['next'])
			except:
				return check_profile

			del check_profile['next']

			merged_data = {key: value for (key, value) in (check_profile.items() + child_data.items())}
			return merged_data

		else:
			return check_profile

	#-----------------------------------
	#helper function for name_show
	def name_show(self, input_key):

		reply = {}

		value = self.namecoind.name_show(input_key)
		
		try:
			profile = json.loads(value.get('value'))
		except:
			profile = value.get('value')

		if utf8len(json.dumps(profile)) > VALUE_MAX_LIMIT:
			new_key = 'i/' + input_key.lstrip('u/') + "-1"
			value2 = self.namecoind.name_show(new_key)  

			if 'code' in value2 and value2.get('code') == -4:
				pass
			else:
				value = value2
		  
		if 'code' in value and value.get('code') == -4:
			return error_reply("Not found", 404)

		for key in value.keys():

			reply['namecoin_address'] = value['address']
			
			if(key == 'value'):
				try:
					reply[key] = json.loads(value[key])
				except:
					reply[key] = value[key]

		return reply

	#-----------------------------------
	#helper function
	def unlock_wallet(self, passphrase, timeout = 100):

		info = self.namecoind.walletpassphrase(passphrase, timeout, True)
		return info             #info will be True or False
