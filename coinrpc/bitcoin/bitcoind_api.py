#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import request, jsonify, abort, Blueprint
bitcoind_api = Blueprint('bitcoind_api', __name__)

from ..config import BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER, BITCOIND_PASSWD, BITCOIND_USE_HTTPS, WALLET_PASSPHRASE

import json
from commontools import pretty_dump, error_reply

from coinrpc.helper import requires_auth

import bitcoinrpc 
from bitcoinrpc.exceptions import *

bitcoind = bitcoinrpc.connect_to_remote(BITCOIND_USER, BITCOIND_PASSWD, host=BITCOIND_SERVER, port=BITCOIND_PORT, use_https=BITCOIND_USE_HTTPS)

import decimal 

#-----------------------------------

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

#-----------------------------------
@bitcoind_api.route('/bitcoind/blocks')
@requires_auth
def blocks():
	reply = {}
	info = bitcoind.getinfo()
	reply['blocks'] = info.blocks
	return pretty_dump(reply)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getblock/<hash>')
@requires_auth
def getblock(hash):
	try:
		info = bitcoind.getblock(hash)
	except InvalidAddressOrKey:				#e.g valid hash is 000000000000000031e5d6e72371d26296cdbf2f7da27ad3f0d462a983675408
		return error_reply("Invalid address or key")

	#json.dumps() gives an exception here: TypeError: Decimal() is not JSON serializable
	return jsonify(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getblockcount')
@requires_auth
def getblockcount():
	info = bitcoind.getblockcount()
	return pretty_dump(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getblockhash/<index>')
@requires_auth
def getblockhash(index):

	try:
		info = bitcoind.getblockhash(int(index))		#e.g valid index is 308728
	except Exception:
		return error_reply("Please make sure index is valid")
		
	return pretty_dump(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getblocknumber')
@requires_auth
def getblocknumber():
	info = bitcoind.getblocknumber()
	return pretty_dump(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getconnectioncount')
@requires_auth
def getconnectioncount():
	info = bitcoind.getconnectioncount()
	return pretty_dump(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getdifficulty')
@requires_auth
def getdifficulty():
	info = bitcoind.getdifficulty()
	return str(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getgenerate')
def getgenerate():
	info = bitcoind.getgenerate()
	return str(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/gethashespersec')
@requires_auth
def gethashespersec():
	info = bitcoind.gethashespersec()
	return str(info)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getinfo')
@requires_auth
def getinfo():
	reply = {}
	info = bitcoind.getinfo()
	
	reply['balance'] = info.balance
	reply['blocks'] = info.blocks
	reply['connections'] = info.connections
	reply['proxy'] = info.proxy
	reply['version'] = info.version
	reply['protocolversion'] = info.protocolversion
	reply['walletversion'] = info.walletversion
	reply['timeoffset'] = info.timeoffset
	reply['testnet'] = info.testnet
	reply['keypoololdest'] = info.keypoololdest
	reply['keypoolsize'] = info.keypoolsize
	reply['keypoololdest'] = info.keypoololdest
	reply['paytxfee'] = info.paytxfee
	reply['errors'] = info.errors

	return json.dumps(reply, cls=DecimalEncoder)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getmininginfo')
@requires_auth
def getmininginfo():
	reply = {}
	info = bitcoind.getmininginfo()

	reply['blocks'] = info.blocks
	reply['currentblocksize'] = info.currentblocksize
	reply['currentblocktx'] = info.currentblocktx
	reply['difficulty'] = info.difficulty
	reply['errors'] = info.errors
	reply['generate'] = info.generate
	reply['genproclimit'] = info.genproclimit
	reply['hashespersec'] = info.hashespersec
	reply['pooledtx'] = info.pooledtx
	reply['testnet'] = info.testnet

	return json.dumps(reply, cls=DecimalEncoder)

#-----------------------------------
@bitcoind_api.route('/bitcoind/getnewaddress')
@requires_auth
def getnewaddress():
	info = bitcoind.getnewaddress()
	return info
