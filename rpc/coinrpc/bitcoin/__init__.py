#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .bitcoind_server import BitcoindServer 

from ..config import BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER, BITCOIND_PASSWD, BITCOIND_USE_HTTPS, WALLET_PASSPHRASE

bitcoind = BitcoindServer(BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER, BITCOIND_PASSWD, BITCOIND_USE_HTTPS, WALLET_PASSPHRASE)