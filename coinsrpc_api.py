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
import namecoinrpc

bitcoind = bitcoinrpc.connect_to_remote(BITCOIND_USER, BITCOIND_PASSWD, host=BITCOIND_SERVER, port=BITCOIND_PORT, use_https=BITCOIND_USE_HTTPS)

namecoind = namecoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, host=NAMECOIND_SERVER, port=NAMECOIND_PORT, use_https=NAMECOIND_USE_HTTPS)


con = Connection()
db = con['namecoin']
domains = db.domains
filtered = db.filtered

#-------------------------
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
    return 'Welcome to the bitcoind/namecoind API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.'	

#-----------------------------------
@app.route('/bitcoind/blocks')
def bitcoind_blocks():
    reply = {}
    info = bitcoind.getinfo()
    reply['blocks'] = info.blocks
    return pretty_dump(reply)

#-----------------------------------
@app.route('/namecoind/blocks')
def namecoind_blocks():
    reply = {}
    info = namecoind.getinfo()
    reply['blocks'] = info.blocks
    return pretty_dump(reply)

#-----------------------------------
@app.route('/namecoind/register_name', methods = ['POST'])
def namecoind_name_new():

    reply = {}
    data = request.values
    
    if not 'name' in data  or not 'value' in data or not 'passphrase' in data:
        return error_reply("Required: name, value, passphrase", 400)
        
    name = data['name']
    value = data['value']
    passphrase = data['passphrase']
    freegraph = False if data.get('freegraph') is None else True   #pass True for freegraph

    #add d/ or u/ based on whether its a domain name or freegraph username
    if not name.startswith('d/') and not name.startswith('u/'):
        if freegraph:
            name = 'u/' + name
        else:
            name = 'd/' + name

    #check if this name already exists
    status = json.loads(namecoind_is_name_registered(name))
    if status['status'] == True:
        return error_reply("This name already exists")
        
    #check if passphrase is valid
    if not unlock_wallet(passphrase):
        return error_reply("Wallet passphrase is incorrect", 403)

    #create new name
    info = namecoind.name_new(name)         #returns a list of [longhex, rand]
    
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
    
    return pretty_dump(reply)

#-----------------------------------
@app.route('/namecoind/name_scan')
def namecoind_name_scan():
    
    start_name = request.args.get('start_name')     
    if start_name == None:
        start_name = "#"

    max_returned = request.args.get('max_returned')
    if max_returned == None:
        max_returned = 500
    else:
        max_returned = int(max_returned)

    info = json.dumps(namecoind.name_scan(start_name, max_returned))
    return pretty_dump(info)

#-----------------------------------
@app.route('/namecoind/fg_scan')
def namecoind_fg_scan():
    
    username = request.args.get('username')     
    if username == None:
        return error_reply("No name given")

    max_returned = 1
    
    users = namecoind.name_scan(username, max_returned)

    for i in users:
        if(i['name'] == username):
            return pretty_dump(i)
    
    return pretty_dump({})

#-----------------------------------
@app.route('/namecoind/transfer_name',  methods = ['POST'])
def transfer_domain():

    reply = {}
    data = request.values

    if not 'name' in data or not 'address' in data or not 'passphrase' in data:    
        return error_reply("Required: name, address, passphrase", 400)
    
    name = data['name']
    address = data['address']
    passphrase = data['passphrase']

    if not name.startswith('d/'):
        name = 'd/' + name
        
    #check if this name exists and if it does, find the value field
    #Note that update command needs an arg of <new value>.
    #In case we're simply transferring, we need to obtain old value first

    name_details = json.loads(namecoind_get_name_details(name))
    if 'code' in name_details and name_details.get('code') == -4:
        return error_reply("Name does not exist")

    value = data.get('value') if data.get('value') is not None else name_details.get('value')

    #now unlock the wallet
    if not unlock_wallet(passphrase):
        error_reply("Wallet passphrase is incorrect", 403)
        
    #transfer the name
    info = namecoind.name_update(name, value, address)
    return pretty_dump(info)

#-----------------------------------
@app.route('/namecoind/is_name_registered/<name>')
def namecoind_is_name_registered(name):
    reply = {}

    if not name.startswith('d/'):
        name = 'd/' + name
    
    info = namecoind.name_show(name)
    
    if 'code' in info and info.get('code') == -4:
        reply['message'] = 'The name is not registered'
        reply['status'] = 404
    else:
        reply['message'] = 'The name is registered'
        reply['status'] = 200
        
    return pretty_dump(reply)

#-----------------------------------
@app.route('/namecoind/get_name_details/<name>')
def namecoind_get_name_details(name):

    if not name.startswith('d/'):
        name = 'd/' + name
        
    info = namecoind.name_show(name)
    return pretty_dump(info)

#-----------------------------------
@app.route('/namecoind/get_filtered_domains')
def namecoind_get_filtered_domains():
    
    info = []
    data = filtered.find();
    for d in data:
        del d['_id']
        info.append(d)
        
    return pretty_dump(info)

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

    reply = {}
    return jsonify(reply)

#-----------------------------------
#helper function
def unlock_wallet(passphrase, timeout = 10):

    info = namecoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False
#-----------------------------------

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)

