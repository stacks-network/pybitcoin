# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .config import NAMECOIND_ENABLED, BITCOIND_ENABLED

if NAMECOIND_ENABLED:
    from .config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER
    from .config import NAMECOIND_PASSWD, NAMECOIND_USE_HTTPS
    from .config import NAMECOIND_WALLET_PASSPHRASE

    from .namecoind_client import NamecoindClient
    namecoind = NamecoindClient(NAMECOIND_SERVER, NAMECOIND_PORT,
                                NAMECOIND_USER, NAMECOIND_PASSWD,
                                NAMECOIND_USE_HTTPS,
                                NAMECOIND_WALLET_PASSPHRASE)


if BITCOIND_ENABLED:
    from .config import BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER
    from .config import BITCOIND_PASSWD, BITCOIND_USE_HTTPS
    from .config import BITCOIND_WALLET_PASSPHRASE

    from .bitcoind_client import BitcoindClient
    bitcoind = BitcoindClient(BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER,
                              BITCOIND_PASSWD, BITCOIND_USE_HTTPS,
                              BITCOIND_WALLET_PASSPHRASE)
