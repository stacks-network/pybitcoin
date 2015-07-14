# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import httplib

from bitcoinrpc.authproxy import AuthServiceProxy

from ..constants import SATOSHIS_PER_COIN

from ..address import script_hex_to_address

from .blockchain_client import BlockchainClient

def create_bitcoind_service_proxy(
    rpc_username, rpc_password, server='127.0.0.1', port=8332, use_https=False):
    """ create a bitcoind service proxy
    """
    protocol = 'https' if use_https else 'http'
    uri = '%s://%s:%s@%s:%s' % (protocol, rpc_username, rpc_password,
        server, port)
    return AuthServiceProxy(uri)

class BitcoindClient(BlockchainClient):
    def __init__(self, rpc_username, rpc_password, use_https=False,
                 server='127.0.0.1', port=8332, version_byte=0):
        self.type = 'bitcoind'
        self.auth = (rpc_username, rpc_password)
        self.bitcoind = create_bitcoind_service_proxy(rpc_username,
            rpc_password, use_https=use_https, server=server, port=port)
        self.version_byte = version_byte

def format_unspents(unspents):
    return [{
        "transaction_hash": s["txid"],
        "output_index": s["vout"],
        "value": int(round(s["amount"]*SATOSHIS_PER_COIN)),
        "script_hex": s["scriptPubKey"],
        "confirmations": s["confirmations"]
        }
        for s in unspents
    ]

def get_unspents(address, blockchain_client):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.

        NOTE: this will only return unspents if the address provided is present
        in the bitcoind server. Use the chain, blockchain, or blockcypher API
        to grab the unspents for arbitrary addresses.
    """
    if isinstance(blockchain_client, BitcoindClient):
        bitcoind = blockchain_client.bitcoind
        version_byte = blockchain_client.version_byte
    elif isinstance(blockchain_client, AuthServiceProxy):
        bitcoind = blockchain_client
        version_byte = 0
    else:
        raise Exception('A BitcoindClient object is required')

    all_unspents = bitcoind.listunspent()

    unspents = []
    for u in all_unspents:
        if 'address' not in u:
            u['address'] = script_hex_to_address(u['scriptPubKey'],
                                                 version_byte=version_byte)
        if 'spendable' in u and u['spendable'] is False:
            continue
        if u['address'] == address:
            unspents.append(u)

    return format_unspents(unspents)


def broadcast_transaction(hex_tx, blockchain_client):
    """ Dispatch a raw transaction to the network.
    """
    if isinstance(blockchain_client, BitcoindClient):
        bitcoind = blockchain_client.bitcoind
    elif isinstance(blockchain_client, AuthServiceProxy):
        bitcoind = blockchain_client
    else:
        raise Exception('A BitcoindClient object is required')

    try:
        resp = bitcoind.sendrawtransaction(hex_tx)
    except httplib.BadStatusLine:
        raise Exception('Invalid HTTP status code from bitcoind.')

    if len(resp) > 0:
        return {'transaction_hash': resp, 'success': True}
    else:
        raise Exception('Invalid response from bitcoind.')
