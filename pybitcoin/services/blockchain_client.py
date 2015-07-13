# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

class BlockchainClient(object):
    """ Type parameter can be 'bitcoind', 'blockchain.info', 'chain.com',
        'blockcypher.com', etc.
        Auth object is a two item tuple.
    """
    def __init__(self, type, auth=None):
        self.type = type
        if isinstance(auth, tuple) and len(auth) == 2:
            self.auth = auth
        else:
            raise Exception('auth must be a two-item tuple')
