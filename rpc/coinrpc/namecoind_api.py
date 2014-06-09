#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import Flask, request, jsonify, make_response, abort, Blueprint
from config import * 

import json

namecoind_api = Blueprint('namecoind_api', __name__)

import pylibmc
from time import time
mc = pylibmc.Client([DEFAULT_HOST + ':' + MEMCACHED_PORT],binary=True)

from functools import wraps

from coinrpc import namecoind_blocks, namecoind_name_new, namecoind_firstupdate, namecoind_name_show

#---------------------------------
def check_auth(username, password):
    return username == APP_USERNAME and password == APP_PASSWORD

#---------------------------------
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return error_reply("invalid username/password")

        elif not check_auth(auth.username, auth.password):
            return error_reply("invalid auth username/password")
        return f(*args, **kwargs)

    return decorated

#---------------------------------
def error_reply(msg, code = -1):
    reply = {}
    reply['status'] = code
    reply['message'] = "ERROR: " + msg
    return jsonify(reply)

#-----------------------------------
@namecoind_api.route('/namecoind/blocks')
def namecoind_api_blocks():
    return jsonify(namecoind_blocks())

#-----------------------------------
@namecoind_api.route('/namecoind/name_show')
def namecoind_api_name_show():
    
    key = request.args.get('key')

    if key == None:
        return error_reply("No key given")

    if MEMCACHED_ENABLED: 
        cache_reply = mc.get("name_" + str(key))
    else:
        cache_reply = None
        print "cache off"

    if cache_reply is None: 
        info = namecoind_name_show(key)
        mc.set("name_" + str(key),json.dumps(info),int(time() + MEMCACHED_TIMEOUT))
        print "cache miss"
    else:
        print "cache hit"
        info = json.loads(cache_reply)

    if 'status' in info:
        if info['status'] == 404:
            abort(404)
            
    return jsonify(info)

#-----------------------------------
@namecoind_api.route('/namecoind/name_new', methods = ['POST'])
#@requires_auth
def namecoind_api_name_new():

    reply = {}
    data = request.values
   
    if not 'key' in data  or not 'value' in data:
        return error_reply("Required: key, value", 400)
        
    key = data['key']
    value = data['value']
    
    return jsonify(namecoind_name_new(key,value))

#----------------------------------------------
@namecoind_api.route('/namecoind/name_firstupdate', methods = ['POST'])
#@requires_auth
def namecoind_api_firstupdate():

    data = request.values

    if not 'key' in data or not 'rand' in data or not 'value' in data:    
        return error_reply("Required: key, value, rand", 400)
    
    tx = None

    if 'tx' in data: 
        tx = data['tx']
    
    return jsonify(namecoind_firstupdate(data['key'],data['rand'],data['value'],tx))

#-----------------------------------
@namecoind_api.route('/namecoind/name_update', methods = ['POST'])
#@requires_auth
def namecoind_api_name_update():

    data = request.values

    if not 'key' in data or not 'new_value' in data:    
        return error_reply("Required: key, new_value", 400)
    
    return jsonify(namecoind_name_update(data['key'],data['value']))

#-----------------------------------
@namecoind_api.route('/namecoind/transfer', methods = ['POST'])
#@requires_auth
def namecoind_api_transfer():

    data = request.values

    if not 'key' in data or not 'new_address' in data:    
        return error_reply("Required: key, new_address", 400)
    
    return jsonify(namecoind_transfer(data['key'],data['new_address']))

