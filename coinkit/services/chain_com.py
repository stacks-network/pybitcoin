# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback

CHAIN_API_BASE_URL = 'https://api.chain.com/v2'

def format_unspents(unspents):
    return [{
        "transaction_hash": s["transaction_hash"],
        "output_index": s["output_index"],
        "value": s["value"],
        "script_opcodes": s["script"],
        "script_hex": s["script_hex"],
        "script_type": s["script_type"],
        "confirmations": s["confirmations"]
        }
        for s in unspents
    ]

def get_unspents(address, auth=None):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    url = CHAIN_API_BASE_URL + '/bitcoin/addresses/' + address + '/unspents'

    if auth:
        r = requests.get(url, auth=auth)
    else:
        r = requests.get(url + '?api-key-id=DEMO-4a5e1e4')

    try:
        unspents = r.json()
    except ValueError, e:
        raise Exception('Invalid response from chain.com.')
    
    return format_unspents(unspents)

def broadcast_transaction(hex_tx, auth=None):
    """ Dispatch a raw hex transaction to the network.
    """
    if not auth or len(auth) != 2:
        raise Exception('Auth required.')

    url = CHAIN_API_BASE_URL + '/bitcoin/transactions'
    payload = json.dumps({ 'hex': hex_tx })
    r = requests.put(url, data=payload, auth=auth)
    
    try:
        data = r.json()
    except ValueError, e:
        raise Exception('Invalid response from chain.com.')

    if 'transaction_hash' in data:
        return {'success': True, 'transaction_hash': data['transaction_hash']}
    else:
        raise Exception('Invalid response from chain.com.')

class ChainClient():
    def __init__(self, api_key_id, api_key_secret):
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret

    def auth(self):
        return (self.api_key_id, self.api_key_secret)

    def get_unspents(self, address):
        return get_unspents(address, auth=self.auth())

    def broadcast_transaction(self, hex_tx):
        return broadcast_transaction(hex_tx, auth=self.auth())
