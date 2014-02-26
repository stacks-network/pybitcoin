#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
    configuration file for coinrpc
'''

import os

DEBUG = True

DEFAULT_PORT =5000
DEFAULT_HOST = '127.0.0.1'

NAMECOIND_USE_HTTPS = True
READ_ONLY_SERVER = False

if READ_ONLY_SERVER:

	NAMECOIND_PORT = 5010
	NAMECOIND_SERVER = '162.243.106.239'
	NAMECOIND_USER ='namecoinrpc'
	NAMECOIND_PASSWD ='68kGrjcLdjMGBiBhh6bW53niCGbFBRrGabHn3KMGsuLb'
	entered_passphrase = ''
else:
	NAMECOIND_PORT = 5005
	NAMECOIND_SERVER = os.environ['NAMECOIND_SERVER']
	NAMECOIND_USER = os.environ['NAMECOIND_USER']
	NAMECOIND_PASSWD = os.environ['NAMECOIND_PASSWD']
	entered_passphrase = os.environ['WALLET_PASSPHRASE']

APP_USERNAME = 'coinrpc'
APP_PASSWORD = 'testingtestingr32fjndfnkgj43rkwbjvfh3jg3jn3'

