#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import bitcoinrpc

from commontools import log

#---------------------------------------
class BitcoindServer(object):

	#-----------------------------------
	def __init__(self, server, port, user, passwd, use_https=True, passphrase=None):
		
		self.passphrase = passphrase
		self.server = server 

		self.bitcoind = bitcoinrpc.connect_to_remote(user, passwd, 
										host=server, port=port, 
										use_https=use_https)

	#-----------------------------------
	def blocks(self):
		reply = {}
		info = self.bitcoind.getinfo()
		reply['blocks'] = info.blocks
		return reply


	#-----------------------------------
	#helper function
	def unlock_wallet(self, passphrase, timeout = 100):

		info = self.bitcoind.walletpassphrase(passphrase, timeout, True)
		return info             #info will be True or False


	#-----------------------------------
	def blocks(self, bitcoin_address, bitcoin_amount):
	
		try:
			status = bitcoind.sendtoaddress(bitcoin_address, float(bitcoin_amount))
			log.debug(status)
		except Exception as e:
			log.debug(str(e))