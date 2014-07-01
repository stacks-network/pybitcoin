#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import Flask, request, jsonify, Response
from pymongo import Connection
from config import * 

app = Flask(__name__)

import json
import bitcoinrpc 
from bitcoinrpc.exceptions import *

bitcoind = bitcoinrpc.connect_to_remote(BITCOIND_USER, BITCOIND_PASSWD, host=BITCOIND_SERVER, port=BITCOIND_PORT, use_https=BITCOIND_USE_HTTPS)

#-----------------------------------
def pretty_dump(input):

    return json.dumps(input, sort_keys=False, indent=4, separators=(',', ': '))

#---------------------------------
def error_reply(msg, code = -1):
    reply = {}
    reply['status'] = code
    reply['message'] = "ERROR: " + msg
    return pretty_dump(reply)

#-----------------------------------
@app.route('/')
def index():
    return 'Welcome to the bitcoind API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.'	

#-----------------------------------
@app.route('/blocks')
def blocks():
    reply = {}
    info = bitcoind.getinfo()
    reply['blocks'] = info.blocks
    return pretty_dump(reply)

#-----------------------------------
@app.route('/getblock/<hash>')
def getblock(hash):
	reply = {}
	try:
		info = bitcoind.getblock(hash)
	except InvalidAddressOrKey:				#e.g valid hash is 000000000000000031e5d6e72371d26296cdbf2f7da27ad3f0d462a983675408
		return error_reply("Invalid address or key")

	#json.dumps() gives an exception here: TypeError: Decimal() is not JSON serializable
	return jsonify(info)

#-----------------------------------
@app.route('/getblockcount')
def getblockcount():
	reply = {}
	info = bitcoind.getblockcount()
	return pretty_dump(info)

#-----------------------------------
@app.route('/getblockhash/<index>')
def getblockhash(index):
	reply = {}

	try:
		info = bitcoind.getblockhash(int(index))		#e.g valid index is 308728
	except Exception:
		return error_reply("Please make sure index is valid")
		
	return pretty_dump(info)

#-----------------------------------
@app.route('/getblocknumber')
def getblocknumber():
	reply = {}
	info = bitcoind.getblocknumber()
	return pretty_dump(info)

#-----------------------------------

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)

