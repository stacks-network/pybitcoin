#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	coinrpc
	~~~~~

	:copyright: (c) 2014 by Halfmoon Labs
	:license: MIT, see LICENSE for more details.
"""

import os
from commontools import log

NAMECOIND_ENABLED = True
BITCOIND_ENABLED = False 

DEBUG = True

#--------------------------------------------------
if NAMECOIND_ENABLED:

	NAMECOIND_USE_HTTPS = True

	try:
		NAMECOIND_PORT = os.environ['NAMECOIND_PORT']
		NAMECOIND_SERVER = os.environ['NAMECOIND_SERVER']
		NAMECOIND_USER = os.environ['NAMECOIND_USER']
		NAMECOIND_PASSWD = os.environ['NAMECOIND_PASSWD']
	except:
		#log.debug("Namecoind not configured")
		NAMECOIND_PORT = 5005
		NAMECOIND_SERVER = NAMECOIND_USER = NAMECOIND_PASSWD = ''

	try:
		NAMECOIND_WALLET_PASSPHRASE = os.environ['NAMECOIND_WALLET_PASSPHRASE']
	except:
		NAMECOIND_WALLET_PASSPHRASE = ''

#--------------------------------------------------
if BITCOIND_ENABLED:

	BITCOIND_USE_HTTPS = True

	try:
		BITCOIND_PORT = os.environ['BITCOIND_PORT']
		BITCOIND_SERVER = os.environ['BITCOIND_SERVER']
		BITCOIND_USER = os.environ['BITCOIND_USER'] 
		BITCOIND_PASSWD = os.environ['BITCOIND_PASSWD']
		BITCOIND_WALLET_PASSPHRASE = os.environ['BITCOIND_WALLET_PASSPHRASE']

	except:
		#log.debug("Bitcoind not configured")
		BITCOIND_PORT = 5005 
		BITCOIND_SERVER = BITCOIND_USER = BITCOIND_PASSWD = ''

	try:
		BITCOIND_WALLET_PASSPHRASE = os.environ['BITCOIND_WALLET_PASSPHRASE']
	except:
		BITCOIND_WALLET_PASSPHRASE = ''