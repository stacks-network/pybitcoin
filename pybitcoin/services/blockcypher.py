# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""


import json
import requests

BLOCKCYPHER_BASE_URL = 'https://api.blockcypher.com/v1/btc/main/'

from .blockchain_client import BlockchainClient


class BlockcypherClient(BlockchainClient):
    def __init__(self, api_key_id=None, api_key_secret=None):
        self.type = 'blockcypher.com'
        if api_key_id and api_key_secret:
            self.auth = (api_key_id, api_key_secret)
        else:
            self.auth = None


def format_unspents(unspents):

    # sandowhich confirmed and unconfiremd unspents
    all_unspents = unspents.get('txrefs', []) + unspents.get('unconfirmed_txrefs', [])

    return [{
        "transaction_hash": s["tx_hash"],
        "output_index": s["tx_output_n"],
        "value": s["value"],
        "script_hex": s.get("script"),
        "confirmations": s["confirmations"],
        }
        for s in all_unspents
    ]


def get_unspents(address, blockchain_client=BlockcypherClient()):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    if not isinstance(blockchain_client, BlockcypherClient):
        raise Exception('A BlockcypherClient object is required')

    url = '%s/addrs/%s?unspentOnly=true&includeScript=true' % (
          BLOCKCYPHER_BASE_URL, address)

    auth = blockchain_client.auth
    if auth:
        r = requests.get(url + '&token=' + auth)
    else:
        r = requests.get(url)

    try:
        unspents = r.json()
    except ValueError:
        raise Exception('Received non-JSON response from blockcypher.com.')

    # sandwhich unconfirmed and confirmed unspents

    return format_unspents(unspents)


def broadcast_transaction(hex_tx, blockchain_client):
    """ Dispatch a raw hex transaction to the network.
    """
    if not isinstance(blockchain_client, BlockcypherClient):
        raise Exception('A BlockcypherClient object is required')

    auth = blockchain_client.auth
    if not auth or len(auth) != 2:
        raise Exception('BlockcypherClient object must have auth credentials.')

    url = '%s/txspush' % BLOCKCYPHER_BASE_URL
    payload = json.dumps({'tx': hex_tx})
    r = requests.put(url, data=payload, auth=auth)

    try:
        data = r.json()
    except ValueError:
        raise Exception('Received non-JSON from blockcypher.com.')

    if 'tx' in data:
        data['success'] = True
        return {'success': True}  # FIXME
    else:
        err_str = 'Tx hash missing from blockcypher response: ' + str(data)
        raise Exception(err_str)
