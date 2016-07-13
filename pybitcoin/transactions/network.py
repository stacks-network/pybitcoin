# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from binascii import hexlify, unhexlify
from bitcoin import sign as sign_transaction

from ..services import blockchain_info, chain_com, bitcoind, blockcypher
from ..privatekey import BitcoinPrivateKey
from .serialize import serialize_transaction, deserialize_transaction
from .outputs import make_pay_to_address_outputs, make_op_return_outputs
from ..constants import STANDARD_FEE, OP_RETURN_FEE

""" Note: for functions that take in an auth object, here are some examples
    for the various APIs available:

    blockcypher.com: auth=(api_key, None) or None
    blockchain.info: auth=(api_key, None)
    chain.com: auth=(api_key_id, api_key_secret)
"""

from ..services import (ChainComClient, BlockchainInfoClient, BitcoindClient,
    BlockcypherClient, BlockchainClient)
from bitcoinrpc.authproxy import AuthServiceProxy


def get_unspents(address, blockchain_client=BlockchainInfoClient()):
    """ Gets the unspent outputs for a given address.
    """
    if isinstance(blockchain_client, BlockcypherClient):
        return blockcypher.get_unspents(address, blockchain_client)
    elif isinstance(blockchain_client, BlockchainInfoClient):
        return blockchain_info.get_unspents(address, blockchain_client)
    elif isinstance(blockchain_client, ChainComClient):
        return chain_com.get_unspents(address, blockchain_client)
    elif isinstance(blockchain_client, (BitcoindClient, AuthServiceProxy)):
        return bitcoind.get_unspents(address, blockchain_client)
    elif hasattr(blockchain_client, "get_unspents"):
        return blockchain_client.get_unspents( address )
    elif isinstance(blockchain_client, BlockchainClient):
        raise Exception('That blockchain interface is not supported.')
    else:
        raise Exception('A BlockchainClient object is required')


def broadcast_transaction(hex_tx, blockchain_client):
    """ Dispatches a raw hex transaction to the network.
    """
    if isinstance(blockchain_client, BlockcypherClient):
        return blockcypher.broadcast_transaction(hex_tx, blockchain_client)
    elif isinstance(blockchain_client, BlockchainInfoClient):
        return blockchain_info.broadcast_transaction(hex_tx, blockchain_client)
    elif isinstance(blockchain_client, ChainComClient):
        return chain_com.broadcast_transaction(hex_tx, blockchain_client)
    elif isinstance(blockchain_client, (BitcoindClient, AuthServiceProxy)):
        return bitcoind.broadcast_transaction(hex_tx, blockchain_client)
    elif hasattr(blockchain_client, "broadcast_transaction"):
        return blockchain_client.broadcast_transaction( hex_tx )
    elif isinstance(blockchain_client, BlockchainClient):
        raise Exception('That blockchain interface is not supported.')
    else:
        raise Exception('A BlockchainClient object is required')


def get_private_key_obj(private_key):
    if isinstance(private_key, BitcoinPrivateKey):
        return private_key
    else:
        return BitcoinPrivateKey(private_key)


def analyze_private_key(private_key, blockchain_client):
    private_key_obj = get_private_key_obj(private_key)
    # determine the address associated with the supplied private key
    from_address = private_key_obj.public_key().address() 
    # get the unspent outputs corresponding to the given address
    inputs = get_unspents(from_address, blockchain_client)
    # return the inputs
    return private_key_obj, from_address, inputs


def make_send_to_address_tx(recipient_address, amount, private_key,
        blockchain_client=BlockchainInfoClient(), fee=STANDARD_FEE,
        change_address=None):
    """ Builds and signs a "send to address" transaction.
    """
    # get out the private key object, sending address, and inputs
    private_key_obj, from_address, inputs = analyze_private_key(private_key,
        blockchain_client)
    # get the change address
    if not change_address:
        change_address = from_address
    # create the outputs
    outputs = make_pay_to_address_outputs(recipient_address, amount, inputs,
                                          change_address, fee=fee)
    # serialize the transaction
    unsigned_tx = serialize_transaction(inputs, outputs)

    # generate a scriptSig for each input
    for i in xrange(0, len(inputs)):
        signed_tx = sign_transaction(unsigned_tx, i, private_key_obj.to_hex())
        unsigned_tx = signed_tx

    # return the signed tx
    return signed_tx


def make_op_return_tx(data, private_key,
        blockchain_client=BlockchainInfoClient(), fee=OP_RETURN_FEE,
        change_address=None, format='bin'):
    """ Builds and signs an OP_RETURN transaction.
    """
    # get out the private key object, sending address, and inputs
    private_key_obj, from_address, inputs = analyze_private_key(private_key,
        blockchain_client)
    # get the change address
    if not change_address:
        change_address = from_address
    # create the outputs
    outputs = make_op_return_outputs(data, inputs, change_address,
        fee=fee, format=format)
    # serialize the transaction
    unsigned_tx = serialize_transaction(inputs, outputs)

    # generate a scriptSig for each input
    for i in xrange(0, len(inputs)):
        signed_tx = sign_transaction(unsigned_tx, i, private_key_obj.to_hex())
        unsigned_tx = signed_tx

    # return the signed tx
    return signed_tx


def send_to_address(recipient_address, amount, private_key,
        blockchain_client=BlockchainInfoClient(), fee=STANDARD_FEE,
        change_address=None):
    """ Builds, signs, and dispatches a "send to address" transaction.
    """
    # build and sign the tx
    signed_tx = make_send_to_address_tx(recipient_address, amount,
        private_key, blockchain_client, fee=fee,
        change_address=change_address)
    # dispatch the signed transction to the network
    response = broadcast_transaction(signed_tx, blockchain_client)
    # return the response
    return response


def embed_data_in_blockchain(data, private_key,
        blockchain_client=BlockchainInfoClient(), fee=OP_RETURN_FEE,
        change_address=None, format='bin'):
    """ Builds, signs, and dispatches an OP_RETURN transaction.
    """
    # build and sign the tx
    signed_tx = make_op_return_tx(data, private_key, blockchain_client,
        fee=fee, change_address=change_address, format=format)
    # dispatch the signed transction to the network
    response = broadcast_transaction(signed_tx, blockchain_client)
    # return the response
    return response


def serialize_sign_and_broadcast(inputs, outputs, private_key,
                                 blockchain_client=BlockchainInfoClient()):
    # extract the private key object
    private_key_obj = get_private_key_obj(private_key)

    # serialize the transaction
    unsigned_tx = serialize_transaction(inputs, outputs)

    # generate a scriptSig for each input
    for i in xrange(0, len(inputs)):
        signed_tx = sign_transaction(unsigned_tx, i, private_key_obj.to_hex())
        unsigned_tx = signed_tx

    # dispatch the signed transaction to the network
    response = broadcast_transaction(signed_tx, blockchain_client)
    # return the response
    return response


def sign_all_unsigned_inputs(hex_privkey, unsigned_tx_hex):
    """
        Sign a serialized transaction's unsigned inputs

        @hex_privkey: private key that should sign inputs
        @unsigned_tx_hex: hex transaction with unsigned inputs

        Returns: signed hex transaction
    """
    inputs, outputs, locktime, version = deserialize_transaction(unsigned_tx_hex)
    tx_hex = unsigned_tx_hex
    for index in xrange(0, len(inputs)):
        if len(inputs[index]['script_sig']) == 0:

            # tx with index i signed with privkey
            tx_hex = sign_transaction(str(unsigned_tx_hex), index, hex_privkey)
            unsigned_tx_hex = tx_hex

    return tx_hex
