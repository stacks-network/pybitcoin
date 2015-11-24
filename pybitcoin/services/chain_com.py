# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback

CHAIN_API_BASE_URL = 'https://api.chain.com/v2'

from .blockchain_client import BlockchainClient

class ChainComClient(BlockchainClient):
    def __init__(self, api_key_id=None, api_key_secret=None):
        self.type = 'chain.com'
        if api_key_id and api_key_secret:
            self.auth = (api_key_id, api_key_secret)
        else:
            self.auth = None

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

def get_unspents(address, blockchain_client=ChainComClient()):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    if not isinstance(blockchain_client, ChainComClient):
        raise Exception('A ChainComClient object is required')

    url = CHAIN_API_BASE_URL + '/bitcoin/addresses/' + address + '/unspents'

    auth = blockchain_client.auth
    if auth:
        r = requests.get(url, auth=auth)
    else:
        r = requests.get(url + '?api-key-id=DEMO-4a5e1e4')

    try:
        unspents = r.json()
    except ValueError, e:
        raise Exception('Received non-JSON response from chain.com.')
    
    return format_unspents(unspents)

def broadcast_transaction(hex_tx, blockchain_client):
    """ Dispatch a raw hex transaction to the network.
    """
    if not isinstance(blockchain_client, ChainComClient):
        raise Exception('A ChainComClient object is required')

    auth = blockchain_client.auth
    if not auth or len(auth) != 2:
        raise Exception('ChainComClient object must have auth credentials.')

    url = CHAIN_API_BASE_URL + '/bitcoin/transactions/send'
    payload = json.dumps({ 'signed_hex': hex_tx })
    r = requests.post(url, data=payload, auth=auth)

    try:
        data = r.json()
    except ValueError, e:
        raise Exception('Received non-JSON from chain.com.')

    if 'transaction_hash' in data:
        reply = {}
        reply['tx_hash'] = data['transaction_hash']
        reply['success'] = True
        return reply
    else:
        raise Exception('Tx hash missing from chain.com response: ' + str(data) + '\noriginal: ' + str(payload))

