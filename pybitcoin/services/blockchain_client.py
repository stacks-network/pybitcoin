# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

class BlockchainClient(object):
    """ type parameter can be 'bitcoind', 'blockchain.info', 'chain.com', etc.
        auth object is a two item tuple
    """
    def __init__(self, type, auth=None):
        self.type = type
        if isinstance(auth, tuple) and len(auth) == 2:
            self.auth = auth
        else:
            raise Exception('auth must be a two-item tuple')
