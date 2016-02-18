# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2015 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os

NAMECOIND_ENABLED = False
BITCOIND_ENABLED = True

DEBUG = True

VALUE_MAX_LIMIT = 520

# --------------------------------------------------
if NAMECOIND_ENABLED:

    NAMECOIND_USE_HTTPS = True

    try:
        NAMECOIND_PORT = os.environ['NAMECOIND_PORT']
        NAMECOIND_SERVER = os.environ['NAMECOIND_SERVER']
        NAMECOIND_USER = os.environ['NAMECOIND_USER']
        NAMECOIND_PASSWD = os.environ['NAMECOIND_PASSWD']
    except:
        # default settings with a public server
        NAMECOIND_PORT = 8332
        NAMECOIND_SERVER = 'nmcd.onename.com'
        NAMECOIND_USER = 'opennamesystem'
        NAMECOIND_PASSWD = 'opennamesystem'

    try:
        NAMECOIND_WALLET_PASSPHRASE = os.environ['NAMECOIND_WALLET_PASSPHRASE']
    except:
        NAMECOIND_WALLET_PASSPHRASE = ''

    try:
        from .config_local import MAIN_SERVER, LOAD_SERVERS
    except:
        MAIN_SERVER = NAMECOIND_SERVER
        LOAD_SERVERS = []

# --------------------------------------------------
if BITCOIND_ENABLED:

    BITCOIND_USE_HTTPS = True

    try:
        BITCOIND_PORT = os.environ['BITCOIND_PORT']
        BITCOIND_SERVER = os.environ['BITCOIND_SERVER']
        BITCOIND_USER = os.environ['BITCOIND_USER']
        BITCOIND_PASSWD = os.environ['BITCOIND_PASSWD']
        BITCOIND_WALLET_PASSPHRASE = os.environ['BITCOIND_WALLET_PASSPHRASE']

    except:
        BITCOIND_SERVER = 'btcd.onename.com'
        BITCOIND_PORT = 8332
        BITCOIND_USER = 'openname'
        BITCOIND_PASSWD = 'opennamesystem'

    try:
        BITCOIND_WALLET_PASSPHRASE = os.environ['BITCOIND_WALLET_PASSPHRASE']
    except:
        BITCOIND_WALLET_PASSPHRASE = ''
