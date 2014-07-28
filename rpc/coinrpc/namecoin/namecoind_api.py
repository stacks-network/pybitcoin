#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import request, jsonify, abort, Blueprint
namecoind_api = Blueprint('namecoind_api', __name__)

from ..config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, WALLET_PASSPHRASE
from ..config import DEFAULT_HOST, MEMCACHED_PORT, MEMCACHED_TIMEOUT, MEMCACHED_ENABLED
from commontools import error_reply

import json

import pylibmc
from time import time
mc = pylibmc.Client([DEFAULT_HOST + ':' + MEMCACHED_PORT],binary=True)

from .namecoind_server import NamecoindServer
namecoind = NamecoindServer(NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, WALLET_PASSPHRASE)

from coinrpc.helper import requires_auth

#-----------------------------------
@namecoind_api.route('/namecoind/name_show')
@requires_auth
def namecoind_api_name_show():

    key = request.args.get('key').lower()

    print key 

    if key == None:
        return error_reply("No key given")

    if MEMCACHED_ENABLED: 
        cache_reply = mc.get("name_" + str(key))
    else:
        cache_reply = None
  
    if cache_reply is None: 
        info = namecoind.name_show(key)
        if MEMCACHED_ENABLED:
            mc.set("name_" + str(key),json.dumps(info),int(time() + MEMCACHED_TIMEOUT))
            #print "cache miss"
    else:
        #print "cache hit"
        info = json.loads(cache_reply)

    if 'status' in info:
        if info['status'] == 404:
            abort(404)
            
    return jsonify(info)

#-----------------------------------
@namecoind_api.route('/namecoind/full_profile')
@requires_auth
def namecoind_api_full_profile():
    
    key = request.args.get('key').lower()

    if key == None:
        return error_reply("No key given")

    if MEMCACHED_ENABLED: 
        cache_reply = mc.get("profile_" + str(key))
    else:
        cache_reply = None
        #print "cache off"

    if cache_reply is None: 

        try:
            info = namecoind.get_full_profile(key)
            jsonify(info)
        except:
            return error_reply("Malformed profile")

        if MEMCACHED_ENABLED:
            mc.set("profile_" + str(key),json.dumps(info),int(time() + MEMCACHED_TIMEOUT))
            #print "cache miss"
    else:
        #print "cache hit"
        info = json.loads(cache_reply)

    if 'status' in info:
        if info['status'] == 404:
            abort(404)
            
    return jsonify(info)