#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from ..config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, NAMECOIND_WALLET_PASSPHRASE

from .namecoind_server import NamecoindServer

namecoind = NamecoindServer(NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER, NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS, NAMECOIND_WALLET_PASSPHRASE)