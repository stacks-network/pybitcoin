#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
"""

import os
from coinrpc.coinrpc_flask import app
from config import DEFAULT_PORT, DEFAULT_HOST, DEBUG, entered_passphrase
import getpass

def runserver():

	port = int(os.environ.get('PORT', DEFAULT_PORT))
	app.run(host=DEFAULT_HOST, port=port, debug=DEBUG)

if __name__ == '__main__':
	runserver()
