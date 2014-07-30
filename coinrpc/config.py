#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
    configuration file
'''

try: 
	from config_local import *
except:

	import os

	DEBUG = True

	DEFAULT_PORT =5000
	DEFAULT_HOST = '127.0.0.1'

	MEMCACHED_PORT = '11211'
	MEMCACHED_TIMEOUT = 15 * 60
	MEMCACHED_ENABLED = False

	#--------------------------------------------------
	NAMECOIND_USE_HTTPS = True

	NAMECOIND_PORT = os.environ['NAMECOIND_PORT']
	NAMECOIND_SERVER = os.environ['NAMECOIND_SERVER']
	NAMECOIND_USER = os.environ['NAMECOIND_USER']
	NAMECOIND_PASSWD = os.environ['NAMECOIND_PASSWD']
	NAMECOIND_WALLET_PASSPHRASE = os.environ['NAMECOIND_WALLET_PASSPHRASE']

	#--------------------------------------------------

	API_USERNAME = os.environ['API_USERNAME']
	API_PASSWORD = os.environ['API_PASSWORD']

	BITCOIND_PORT = os.environ['BITCOIND_PORT']
	BITCOIND_SERVER = os.environ['BITCOIND_SERVER']
	BITCOIND_USER = os.environ['BITCOIND_USER'] 
	BITCOIND_PASSWD = os.environ['BITCOIND_PASSWD']
	BITCOIND_WALLET_PASSPHRASE = os.environ['BITCOIND_WALLET_PASSPHRASE']

	BITCOIND_USE_HTTPS = True

