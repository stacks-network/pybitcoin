#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	coinrpc
	~~~~~

	:copyright: (c) 2014 by Halfmoon Labs
	:license: MIT, see LICENSE for more details.
"""

VALUE_MAX_LIMIT = 520

import json
from commontools import utf8len, error_reply, log

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

#---------------------------------------
class NamecoindServer(object):

	#-----------------------------------
	def __init__(self, server, port, user, passwd, use_https=True, passphrase=None):
		
		self.passphrase = passphrase
		self.server = server

		if use_https:
			http_string = 'https://'
		else:
			http_string = 'http://'

		self.namecoind = AuthServiceProxy(http_string + user + ':' + passwd + '@' + server + ':' + str(port))

	#-----------------------------------
	def blocks(self):

		info = self.namecoind.getinfo()
		return info['blocks']

	#-----------------------------------
	
	def name_filter(self,regex,check_blocks=36000,show_from=0,num_results=0):

		info = self.namecoind.name_filter(regex,check_blocks,show_from,num_results)
		return info

	#-----------------------------------
	#step-1 for registrering new names 
	def name_new(self, key,value,force_registration=False):
		
		#check if this key already exists
		if self.check_registration(key) and not force_registration:
			return error_reply("This key already exists")
			
		#check if passphrase is valid
		if not self.unlock_wallet(self.passphrase):
			return error_reply("Error unlocking wallet", 403)

		#create new name
		#returns a list of [longhex, rand]
		try:
			info = self.namecoind.name_new(key)
		except JSONRPCException as e:
			return e.error
			
		return info

	#----------------------------------------------
	#step-2 for registering 
	def firstupdate(self, key,rand,value,tx=None):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Error unlocking wallet", 403)

		try:
			if tx is not None: 
				info = self.namecoind.name_firstupdate(key, rand, tx, value)
			else:
				info = self.namecoind.name_firstupdate(key, rand, value)
		except JSONRPCException as e:
			return e.error
				
		return info

	#-----------------------------------
	def name_update(self, key,value):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#now unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Error unlocking wallet", 403)
			
		#update the 'value'
		try:
			info = self.namecoind.name_update(key, value)
		except JSONRPCException as e:
			return e.error

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
			error_reply("Error unlocking wallet", 403)
		
		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#transfer the name (underlying call is still name_update)
		info = self.namecoind.name_update(key, value, new_address)

		return info

	#-----------------------------------
	def check_registration(self, key):

		try:
			info = self.namecoind.name_show(key)
		except JSONRPCException as e:
			info = e.error
			
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
	def name_show(self, input_key):

		reply = {}

		try:
			value = self.namecoind.name_show(input_key)
		except JSONRPCException as e:
			return e.error
		
		try:
			profile = json.loads(value.get('value'))
		except:
			profile = value.get('value')
  
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

		try:
			info = self.namecoind.walletpassphrase(passphrase, timeout)
		except JSONRPCException as e:
			if e.error['code'] == -17:
				return True
			else:
				log.debug(e.error)
				return False

		return True

	#-----------------------------------
	def importprivkey(self, namecoinprivkey,label='import',rescan=False):
	
		self.unlock_wallet(self.passphrase)

		info = self.namecoind.importprivkey(namecoinprivkey,label,rescan)

		return info
	