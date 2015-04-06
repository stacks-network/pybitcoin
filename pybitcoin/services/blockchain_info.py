# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback
from ..hash import reverse_hash

BLOCKCHAIN_API_BASE_URL = "https://blockchain.info"

from .blockchain_client import BlockchainClient

class BlockchainInfoClient(BlockchainClient):
    def __init__(self, api_key=None):
        self.type = 'blockchain.info'
        if api_key:
            self.auth = (api_key, '')
        else:
            self.auth = None

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

def get_unspents(address, blockchain_client=BlockchainInfoClient()):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    if not isinstance(blockchain_client, BlockchainInfoClient):
        raise Exception('A BlockchainInfoClient object is required')

    url = BLOCKCHAIN_API_BASE_URL + "/unspent?format=json&active=" + address

    auth = blockchain_client.auth
    if auth and len(auth) == 2 and isinstance(auth[0], str):
        url = url + "&api_code=" + auth[0]

    r = requests.get(url, auth=auth)
    try:
        unspents = r.json()["unspent_outputs"]
    except ValueError, e:
        raise Exception('Invalid response from blockchain.info.')
    
    return format_unspents(unspents)

def broadcast_transaction(hex_tx, blockchain_client=BlockchainInfoClient()):
    """ Dispatch a raw transaction to the network.
    """
    url = BLOCKCHAIN_API_BASE_URL + '/pushtx'
    payload = {'tx': hex_tx}
    r = requests.post(url, data=payload, auth=blockchain_client.auth)
    
    if 'submitted' in r.text.lower():
        return {'success': True}
    else:
        raise Exception('Invalid response from blockchain.info.')


