#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import bitcoinrpc

from commontools import log, error_reply

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
	def unlock_wallet(self, timeout = 120):

		info = self.bitcoind.walletpassphrase(self.passphrase, timeout, True)
		return info             #info will be True or False


	#-----------------------------------
	def sendtoaddress(self, bitcoinaddress, amount):
	
		try:
			status = self.bitcoind.sendtoaddress(bitcoinaddress, float(amount))
			log.debug(status)
			return status 
		except Exception as e:
			log.debug(str(e))
			return error_reply(str(e))

	#-----------------------------------
	def validateaddress(self, bitcoinaddress):
	
		try:
			status = self.bitcoind.validateaddress(bitcoinaddress)
			log.debug(status)
			return status
		except Exception as e:
			log.debug(str(e))
			return error_reply(str(e))

	#-----------------------------------
	def importprivkey(self, bitcoinprivkey, label='', rescan=False):
	
		try:
			if rescan is True: 
				status = self.bitcoind.importprivkey(bitcoinprivkey, label, True)
			else:
				status = self.bitcoind.importprivkey(bitcoinprivkey, label, False) 
			log.debug(status)
			return status
		except Exception as e:
			log.debug(str(e))
			return error_reply(str(e))
