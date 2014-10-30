# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from ..services import blockchain_info, blockcypher_com, chain_com

def get_unspents(address, api='blockchain.info', auth=None):
    """ The optional auth object is a 2-item tuple.
        For blockchain.info, auth=(api_key, None)
        For chain.com, auth=(api_key_id, api_key_secret)
    """
    if api == 'blockchain.info':
        return blockchain_info.get_unspents(address, auth=auth)
    elif api == 'chain.com':
        return chain_com.get_unspents(address, auth=auth)
    elif api == 'blockcypher.com':
        return blockcypher_com.get_unspents(address, auth=auth)
    else:
        raise Exception('API not supported.')
