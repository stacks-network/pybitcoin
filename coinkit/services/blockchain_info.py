# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback
from ..hash import reverse_hash

BLOCKCHAIN_API_BASE_URL = "https://blockchain.info"

def format_unspents(unspents):
    return [{
        "transaction_hash": reverse_hash(s["tx_hash"]),
        "output_index": s["tx_output_n"],
        "value": s["value"],
        "script_hex": s["script"],
        "confirmations": s["confirmations"]
        }
        for s in unspents
    ]

def get_unspents(address, auth=None):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    url = BLOCKCHAIN_API_BASE_URL + "/unspent?format=json&active=" + address

    if auth and len(auth) == 2 and isinstance(auth[0], str):
        url = url + "&api_code=" + auth[0]

    r = requests.get(url, auth=auth)
    try:
        unspents = r.json()["unspent_outputs"]
    except ValueError, e:
        raise Exception('Invalid response from blockchain.info.')
    
    return format_unspents(unspents)

def broadcast_transaction(hex_tx, auth=None):
    """ Dispatch a raw transaction to the network.
    """
    url = BLOCKCHAIN_API_BASE_URL + '/pushtx'
    payload = {'tx': hex_tx}
    r = requests.post(url, data=payload)
    
    if 'submitted' in r.text.lower():
        return {'success': True}
    else:
        raise Exception('Invalid response from blockchain.info.')

class BlockchainClient():
    def __init__(self, api_key):
        self.api_key = api_key

    def auth(self):
        return (self.api_key, '')

    def get_unspents(self, address):
        return get_unspents(address, auth=self.auth())

    def broadcast_transaction(self, hex_tx):
        return broadcast_transaction(hex_tx, auth=self.auth())
