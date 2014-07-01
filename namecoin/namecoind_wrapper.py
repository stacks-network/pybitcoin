#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS
from config import WALLET_PASSPHRASE

VALUE_MAX_LIMIT = 520

import json
import namecoinrpc

namecoind = namecoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, 
                                        host=NAMECOIND_SERVER, port=NAMECOIND_PORT, 
                                        use_https=NAMECOIND_USE_HTTPS)

#-----------------------------------
def utf8len(s):

    if type(s) == unicode:
        return len(s)
    else:
        return len(s.encode('utf-8'))

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
    if not unlock_wallet(WALLET_PASSPHRASE):
        return error_reply("Wallet passphrase is incorrect", 403)

    #create new name
    #returns a list of [longhex, rand]
    info = namecoind.name_new(key)
    
    return info

#----------------------------------------------
#step-2 for registering 
def namecoind_firstupdate(key,rand,value,tx=None):

    if utf8len(value) > VALUE_MAX_LIMIT:
        return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

    #unlock the wallet
    if not unlock_wallet(WALLET_PASSPHRASE):
        error_reply("Wallet passphrase is incorrect", 403)

    if tx is not None: 
        info = namecoind.name_firstupdate(key, rand, value, tx)
    else:
        info = namecoind.name_firstupdate(key, rand, value)

    return info

#-----------------------------------
def namecoind_name_update(key,value):

    if utf8len(value) > VALUE_MAX_LIMIT:
        return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

    #now unlock the wallet
    if not unlock_wallet(WALLET_PASSPHRASE):
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
    if not unlock_wallet(WALLET_PASSPHRASE):
        error_reply("Wallet passphrase is incorrect", 403)
    
    if utf8len(value) > VALUE_MAX_LIMIT:
        return error_reply("value larger than " + str(VALUE_MAX_LIMIT))

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
def get_full_profile(key):

    check_profile = namecoind_name_show(key)
    
    try:
        check_profile = check_profile['value']
    except:
        return check_profile
                
    if 'next' in check_profile:
        child_data = get_full_profile(check_profile['next'])

        del check_profile['next']

        merged_data = {key: value for (key, value) in (check_profile.items() + child_data.items())}
        return merged_data

    else:
        return check_profile

#-----------------------------------
#helper function for name_show
def namecoind_name_show(input_key):

    reply = {}

    value = namecoind.name_show(input_key)
    
    try:
        profile = json.loads(value.get('value'))
    except:
        profile = value.get('value')

    if utf8len(json.dumps(profile)) > VALUE_MAX_LIMIT:
        new_key = 'i/' + input_key.lstrip('u/') + "-1"
        value2 = namecoind.name_show(new_key)  

        if 'code' in value2 and value2.get('code') == -4:
            pass
        else:
            value = value2
      
    if 'code' in value and value.get('code') == -4:
        return error_reply("Not found", 404)

    for key in value.keys():

        reply['namecoin_address'] = value['address']
        
        if(key == 'value'):
            try:
                reply[key] = json.loads(value[key])
            except:
                reply[key] = value[key]

    return reply

#-----------------------------------
#helper function
def unlock_wallet(passphrase, timeout = 100):

    info = namecoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False
