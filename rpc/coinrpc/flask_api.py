# -*- coding: utf-8 -*-
"""
    flask API
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
"""

from flask import Flask, make_response, jsonify
import json 

from namecoin.namecoind_api import namecoind_api

app = Flask(__name__)

app.register_blueprint(namecoind_api)

#-----------------------------------
@app.route('/')
def index():
    return '<hmtl><body>Welcome to the coinrpc API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.</body></html>'

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return json.dumps(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)
