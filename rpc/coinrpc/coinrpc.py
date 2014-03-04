#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from config import * 

import json
import namecoinrpc

namecoind = namecoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, 
                                        host=NAMECOIND_SERVER, port=NAMECOIND_PORT, 
                                        use_https=NAMECOIND_USE_HTTPS)


#---------------------------------
def error_reply(msg, code = -1):
    reply = {}
    reply['status'] = code
    reply['message'] = "ERROR: " + msg
    return reply 

#-----------------------------------
def namecoind_blocks():
    reply = {}
    info = namecoind.getinfo()
    reply['blocks'] = info.blocks
    return reply

#-----------------------------------
#step-1 for registrering new names 
def namecoind_name_new(key,value):
  
    #check if this key already exists
    if check_registration(key):
        return error_reply("This key already exists")
        
    #check if passphrase is valid
    if not unlock_wallet(entered_passphrase):
        return error_reply("Wallet passphrase is incorrect", 403)

    #create new name
    #returns a list of [longhex, rand]
    info = namecoind.name_new(key)
    
    return info

#----------------------------------------------
#step-2 for registering 
def namecoind_firstupdate(key,rand,value,tx=None):

    #unlock the wallet
    if not unlock_wallet(entered_passphrase):
        error_reply("Wallet passphrase is incorrect", 403)

    if tx is not None: 
        info = namecoind.name_firstupdate(key, rand, value, tx)
    else:
        info = namecoind.name_firstupdate(key, rand, value)

    return info

#-----------------------------------
def namecoind_name_update(key,value):
    
    #now unlock the wallet
    if not unlock_wallet(entered_passphrase):
        error_reply("Wallet passphrase is incorrect", 403)
        
    #update the 'value'
    info = namecoind.name_update(key, value)

    return info

#-----------------------------------
def namecoind_transfer(key,new_address,value=None):
 
    #check if this name exists and if it does, find the value field
    #note that update command needs an arg of <new value>.
    #in case we're simply transferring, we need to obtain old value first

    key_details = namecoind_name_show(key)

    if 'code' in key_details and key_details.get('code') == -4:
        return error_reply("Key does not exist")

    #get new 'value' if given, otherwise use the old 'value'
    if value is None: 
        value = json.dumps(key_details['value'])

    #now unlock the wallet
    if not unlock_wallet(entered_passphrase):
        error_reply("Wallet passphrase is incorrect", 403)
    
    #transfer the name (underlying call is still name_update)
    info = namecoind.name_update(key, value, new_address)

    return info

#-----------------------------------
def check_registration(key):

    info = namecoind.name_show(key)
    
    if 'code' in info and info.get('code') == -4:
        return False
    elif 'expired' in info and info.get('expired') == 1:
        return False
    else:
        return True

#-----------------------------------
def validate_address(address):

    reply = {}
    info = namecoind.validateaddress(address)
    if info.get('isvalid'):
        reply['message'] = 'The address is valid'
        reply['status'] = 200
    else:
        reply['message'] = 'The address is not valid'
        reply['status'] = 404

    return jsonify(reply)

#-----------------------------------
#helper function for name_show
def namecoind_name_show(input_key):

    reply = {}

    max_returned = 1

    value = namecoind.name_show(input_key)

    if 'code' in value and value.get('code') == -4:
        return error_reply("Not found", 404)

    for key in value.keys():
        
        if(key == 'value'):
            try:
                reply[key] = json.loads(value[key])
            except:
                reply[key] = value[key]

    return reply

#-----------------------------------
#helper function
def unlock_wallet(passphrase, timeout = 10):

    info = namecoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False
