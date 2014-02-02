#!/usr/bin/env python
#-----------------------
# Copyright 2013 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import Flask, request, jsonify
from pymongo import Connection
from config import * 

app = Flask(__name__)

import json
import bitcoinrpc 

bitcoind = bitcoinrpc.connect_to_remote(BITCOIND_USER, BITCOIND_PASSWD, 
									host=BITCOIND_SERVER, port=BITCOIND_PORT, use_https=BITCOIND_USE_HTTPS)

namecoind = bitcoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, 
									host=NAMECOIND_SERVER, port=NAMECOIND_PORT, use_https=NAMECOIND_USE_HTTPS)

con = Connection()
db = con['namecoin']
domains = db.domains
filtered = db.filtered

#-----------------------------------
@app.route('/')
def index():
    return 'Welcome to the bitcoind/namecoind API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.'	

#-----------------------------------
@app.route('/bitcoind/blocks')
def bitcoind_blocks():
    reply = {}
    info = bitcoind.getinfo()
    reply['blocks'] = info.blocks
    return jsonify(reply)

#-----------------------------------
@app.route('/namecoind/blocks')
def namecoind_blocks():
    reply = {}
    info = namecoind.getinfo()
    reply['blocks'] = info.blocks
    return jsonify(reply)

#-----------------------------------
@app.route('/namecoind/register_name/<name>/<value>/<passphrase>')
def namecoind_name_new(name, value, passphrase):

    reply = {}

    #check if passphrase is valid
    if not unlock_wallet(passphrase):
        reply['code'] = 403
        reply['message'] = "Wallet passphrase is incorrect"
        return jsonify(reply)

    if not name.startswith('d/'):
        name = 'd/' + name
        
    #info = ['ads', 'adsadasd']
    info = namecoind.name_new(name)
    
    reply['longhex'] = info[0]
    reply['rand'] = info[1]
    reply['name'] = name
    reply['value'] = value
    
    #get current block...
    info = namecoind.getinfo()
    reply['current_block'] = info.blocks
    reply['wait_till_block'] = info.blocks + 12
    reply['activated'] = False
    
    #save this data to Mongodb...
    domains.insert(reply)

    reply['message'] = 'Your domain will be activated in roughly two hours'
    del reply['_id']        #reply[_id] is causing a json encode error
    
    return jsonify(reply)

#-----------------------------------
@app.route('/namecoind/name_scan')
def namecoind_name_scan():
    reply = {}

    start_name = request.args.get('start_name')     
    if start_name == None:
            start_name = "g/m"

    max_returned = request.args.get('max_returned')
    if max_returned == None:
            max_returned = 500
    else:
            max_returned = int(max_returned)

    info = namecoind.name_scan(start_name, max_returned)
    reply = info
    return jsonify(reply)

#-----------------------------------
@app.route('/namecoind/is_name_registered/<name>')
def namecoind_is_name_registered(name):
    reply = {}

    info = namecoind.name_show(name)
    if 'code' in info and info.get('code') == -4:
        reply['message'] = 'The name is not registered'
        reply['code'] = 'No'
    else:
        reply['message'] = 'The name is registered'
        reply['code'] = 'Yes'
        
    return jsonify(reply)

#-----------------------------------
@app.route('/namecoind/get_name_details/<name>')
def namecoind_get_name_details(name):
    
    info = namecoind.name_show(name)
    return jsonify(info)

#-----------------------------------
@app.route('/namecoind/get_filtered_domains')
def namecoind_get_filtered_domains():

    info = []
    data = filtered.find();
    for d in data:
        del d['_id']
        info.append(d)
        
    return jsonify(info)

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

    reply = {}
    return jsonify(reply)

#-----------------------------------
#helper function
def namecoind_firstupdate(name, rand, value):
    
    info = namecoind.name_firstupdate(name, rand, value)
    return jsonify(info)

#-----------------------------------
#helper function
#@app.route('/passphrase/<passphrase>')
def unlock_wallet(passphrase, timeout = 10):

    info = namecoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False
#-----------------------------------

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)

