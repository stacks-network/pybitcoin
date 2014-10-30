# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from ..services import blockchain_info, blockcypher_com, chain_com

def get_unspents(address, api='blockchain.info'):
    if api == 'blockchain.info':
        return blockchain_info.get_unspents(address)
    elif api == 'chain.com':
        return chain_com.get_unspents(address)
    elif api == 'blockcypher.com':
        return blockcypher_com.get_unspents(address)
    else:
        raise Exception('API not supported.')
