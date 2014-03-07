#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pymongo import Connection
from coinrpc.coinrpc import namecoind_transfer, namecoind_name_show, check_registration

con = Connection()
db = con['namecoin']
remoteusers = db.remoteusers

#-----------------------------------
def test_private_key(passphrase,nmc_address):

	from coinkit.keypair import NamecoinKeypair

	keypair = NamecoinKeypair.from_passphrase(passphrase)
	
	#print keypair.wif_pk()
	
	generated_nmc_address = keypair.address()

	if(generated_nmc_address == nmc_address):
		return True
	else:
		return False

#-----------------------------------
def do_name_transfer(username):

	try:
		entry = remoteusers.find_one({'username':username})
		nmc_address = entry['namecoin_address']
	except:
		print "no such user in DB"
		return 
	
	key = 'u/' + username

	if check_registration(key):

		value = namecoind_name_show(key)['value']

		next_blob = value['next']

		#namecoind_transfer(key,nmc_address)
		print key, nmc_address

		if next_blob is not None: 
			print next_blob, nmc_address
			#namecoind_transfer(next_blob,nmc_address)	
	else:	
		print "activate the name first"

#-----------------------------------
if __name__ == '__main__':

	username = 'taylorfrancis'
   	do_name_transfer(username)

