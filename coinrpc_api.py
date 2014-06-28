#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

from flask import Flask, make_response, jsonify
from config import DEFAULT_PORT, DEFAULT_HOST, DEBUG 
import json 

from namecoin.namecoind_api import namecoind_api
from checker.checker_api import checker_api 

app = Flask(__name__)

app.register_blueprint(namecoind_api)
app.register_blueprint(checker_api)

#-----------------------------------
@app.route('/')
def index():
    return 'Welcome to the namecoind API server of <a href="http://halfmoonlabs.com">Halfmoon Labs</a>.'

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return json.dumps(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

#-----------------------------------
if __name__ == '__main__':

	app.run(host=DEFAULT_HOST, port=DEFAULT_PORT,debug=DEBUG)