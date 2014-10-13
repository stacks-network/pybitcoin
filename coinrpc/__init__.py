#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.

	two use cases of coinrpc:
	a) get access to a namecoind server (read/write)
	b) get access to a bitcoind server (read/write)
"""

from .config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, NAMECOIND_WALLET_PASSPHRASE
from .namecoind_server import NamecoindServer
namecoind = NamecoindServer(NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, NAMECOIND_WALLET_PASSPHRASE)

from .config import BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER, BITCOIND_PASSWD, BITCOIND_USE_HTTPS, BITCOIND_WALLET_PASSPHRASE
from .bitcoind_server import BitcoindServer 
bitcoind = BitcoindServer(BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER, BITCOIND_PASSWD, BITCOIND_USE_HTTPS, BITCOIND_WALLET_PASSPHRASE)