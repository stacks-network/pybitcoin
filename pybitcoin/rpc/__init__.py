# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2015 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .config import NAMECOIND_ENABLED, BITCOIND_ENABLED

if NAMECOIND_ENABLED:

    from .namecoind_client import NamecoindClient
    namecoind = NamecoindClient()  # start with default server settings


if BITCOIND_ENABLED:

    from .bitcoind_client import BitcoindClient
    bitcoind = BitcoindClient()  # start with default server settings
