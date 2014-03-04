#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import Flask, request, jsonify, make_response, abort
from config import * 

app = Flask(__name__)

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
@app.route('/')
def index():
    return 'Welcome to the namecoind API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.'	

#-----------------------------------
@app.route('/namecoind/blocks')
def namecoind_api_blocks():
    return jsonify(namecoind_blocks())

#-----------------------------------
@app.route('/namecoind/name_new', methods = ['POST'])
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
@app.route('/namecoind/name_firstupdate', methods = ['POST'])
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
@app.route('/namecoind/name_update', methods = ['POST'])
#@requires_auth
def namecoind_api_name_update():

    data = request.values

    if not 'key' in data or not 'new_value' in data:    
        return error_reply("Required: key, new_value", 400)
    
    return jsonify(namecoind_name_update(data['key'],data['value']))

#-----------------------------------
@app.route('/namecoind/transfer', methods = ['POST'])
#@requires_auth
def namecoind_api_transfer():

    data = request.values

    if not 'key' in data or not 'new_address' in data:    
        return error_reply("Required: key, new_address", 400)
    
    return jsonify(namecoind_transfer(data['key'],data['new_address']))

#-----------------------------------
@app.route('/namecoind/name_show')
def namecoind_api_name_show():
    
    key = request.args.get('key')

    if key == None:
        return error_reply("No key given")

    info = namecoind_name_show(key)

    if 'status' in info:
        if info['status'] == 404:
            abort(404)
            
    return jsonify(info)

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

    reply = {}
    return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

#-----------------------------------
if __name__ == '__main__':
    
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)
