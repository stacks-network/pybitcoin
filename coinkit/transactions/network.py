# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from binascii import hexlify, unhexlify
from pybitcointools import sign as sign_transaction

from ..services import blockchain_info, blockcypher_com, chain_com
from ..privatekey import BitcoinPrivateKey
from .serialize import make_pay_to_address_transaction

""" Note: for functions that take in an auth object, here are some examples
    for the various APIs available:
    
    blockchain.info: auth=(api_key, None)
    chain.com: auth=(api_key_id, api_key_secret)
"""

def get_unspents(address, api='blockchain.info', auth=None):
    """ Gets the unspent outputs for a given address.

        The optional auth object is a 2-item tuple.
    """
    if api == 'blockchain.info':
        return blockchain_info.get_unspents(address, auth=auth)
    elif api == 'chain.com':
        return chain_com.get_unspents(address, auth=auth)
    elif api == 'blockcypher.com':
        return blockcypher_com.get_unspents(address, auth=auth)
    else:
        raise Exception('API not supported.')

def broadcast_transaction(hex_transaction, api='chain.com', auth=None):
    """ Dispatches a raw hex transaction to the network.

        Auth object is a 2-item tuple.
    """
    if api == 'chain.com':
        return chain_com.send_transaction(hex_transaction, auth=auth)
    elif api == 'blockchain.info':
        return blockchain_info.send_transaction(hex_transaction, auth=auth)
    else:
        raise Exception('API not supported.')

def send_to_address(to_address, amount, sender_private_key, auth,
                    api='chain.com'):
    """ Builds a transaction, signs it, and dispatches it to the network.

        Auth object is a 2-item tuple.
    """
    # determine the address associated with the supplied private key
    from_address = BitcoinPrivateKey(sender_private_key).public_key().address()
    # get the unspent outputs corresponding to the given address
    inputs = get_unspents(from_address)
    # create an unsigned transaction from the inputs, to address, & amount
    unsigned_hex_transaction = make_send_to_address_transaction(inputs,
        from_address, to_address, amount)
    # signs the unsigned transaction with the private key
    signed_hex_transaction = sign_transaction(unsigned_hex_transaction, 0,
        sender_private_key)
    # dispatch the signed transction to the network
    response = broadcast_transaction(signed_hex_transaction, api=api, auth=auth)
    # return the response
    return response

