#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	coinrpc
	~~~~~

	:copyright: (c) 2014 by Halfmoon Labs
	:license: MIT, see LICENSE for more details.
"""

VALUE_MAX_LIMIT = 520

from commontools import utf8len, error_reply, get_json

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from coinrpc.config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_WALLET_PASSPHRASE, NAMECOIND_USE_HTTPS

#---------------------------------------
class NamecoindServer(object):

	#-----------------------------------
	def __init__(self, server=NAMECOIND_SERVER, port=NAMECOIND_PORT, user=NAMECOIND_USER, 
					passwd=NAMECOIND_PASSWD, use_https=NAMECOIND_USE_HTTPS, passphrase=NAMECOIND_WALLET_PASSPHRASE):
		
		if use_https:
			http_string = 'https://'
		else:
			http_string = 'http://'

		self.obj = AuthServiceProxy(http_string + user + ':' + passwd + '@' + server + ':' + str(port))

		self.passphrase = passphrase
		self.server = server

	#-----------------------------------
	#changes the behavior of underlying authproxy to return the error from namecoind instead of raising JSONRPCException
	def __getattr__(self, name):
		func = getattr(self.__dict__['obj'], name)
		if callable(func):
			def my_wrapper(*args, **kwargs):
				try:
					ret = func(*args, **kwargs)
				except JSONRPCException as e:
					return e.error
				else:
					return ret
			return my_wrapper
		else:
			return func

	#-----------------------------------
	def blocks(self):

		info = self.getinfo()
		return info['blocks']

	#-----------------------------------
	def name_filter(self,regex,check_blocks=36000,show_from=0,num_results=0):

		info = self.obj.name_filter(regex,check_blocks,show_from,num_results)
		return info

	#-----------------------------------
	#step-1 for registrering new names 
	def name_new(self, key,value):
		
		#check if this key already exists
		#namecoind lets you do name_new on keys that exist
		if self.check_registration(key):
			return error_reply("This key already exists")
			
		#check if passphrase is valid
		if not self.unlock_wallet(self.passphrase):
			return error_reply("Error unlocking wallet", 403)

		#create new name
		#returns a list of [tx, rand]
		info = self.obj.name_new(key)
		
		return info

	#----------------------------------------------
	#step-2 for registering 
	def firstupdate(self, key,rand,value,tx=None):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Error unlocking wallet", 403)

		if tx is not None: 
			info = self.obj.name_firstupdate(key, rand, tx, value)
		else:
			info = self.obj.name_firstupdate(key, rand, value)
				
		return info

	#-----------------------------------
	def name_update(self, key, value):

		if utf8len(value) > VALUE_MAX_LIMIT:
			return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

		#now unlock the wallet
		if not self.unlock_wallet(self.passphrase):
			error_reply("Error unlocking wallet", 403)
			
		#update the 'value'
		info = self.obj.name_update(key, value)
		
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

		#transfer the name (underlying call is still name_update)
		info = self.name_update(key, value, new_address)

		return info

	#-----------------------------------
	def check_registration(self, key):

		info = self.name_show(key)
			
		if 'code' in info and info.get('code') == -4:
			return False
		elif 'expired' in info and info.get('expired') == 1:
			return False
		else:
			return True

	#-----------------------------------
	def validate_address(self, address):

		info = self.validateaddress(address)
		
		info['server'] = self.server

		return info

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

		try:
			reply = self.obj.name_show(input_key)
		except JSONRPCException as e:
			return e.error
		
		reply['value'] = get_json(reply['value'])

		return reply

	#-----------------------------------
	def unlock_wallet(self, passphrase, timeout = 100):

		try:
			reply = self.walletpassphrase(passphrase, timeout)
		except JSONRPCException as e:
			if 'code' in reply:
				if reply['code'] == -17:
					return True
				else:
					return False

		return True

	#-----------------------------------
	def importprivkey(self, namecoinprivkey,label='import',rescan=False):
	
		if not self.unlock_wallet(self.passphrase):
			error_reply("Error unlocking wallet", 403)
		
		try:
			reply = self.obj.importprivkey(namecoinprivkey,label,rescan)
		except JSONRPCException as e:
			return e.error
		
		return reply