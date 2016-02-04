# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2016 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from commontools import log, error_reply
from .. import SATOSHIS_PER_COIN
from .. import script_hex_to_address

from .config import BITCOIND_SERVER, BITCOIND_PORT, BITCOIND_USER
from .config import BITCOIND_PASSWD, BITCOIND_WALLET_PASSPHRASE
from .config import BITCOIND_USE_HTTPS


class BitcoindClient(object):

    def __init__(self, server=BITCOIND_SERVER, port=BITCOIND_PORT,
                 user=BITCOIND_USER, passwd=BITCOIND_PASSWD,
                 use_https=BITCOIND_USE_HTTPS,
                 passphrase=BITCOIND_WALLET_PASSPHRASE, version_byte=0):

        self.passphrase = passphrase
        self.server = server

        self.type = 'bitcoind'
        self.version_byte = version_byte

        if use_https:
            http_string = 'https://'
        else:
            http_string = 'http://'

        self.obj = AuthServiceProxy(http_string + user + ':' + passwd +
                                    '@' + server + ':' + str(port))

    def __getattr__(self, name):
        """ changes the behavior of underlying authproxy to return the error
            from bitcoind instead of raising JSONRPCException
        """
        func = getattr(self.__dict__['obj'], name)
        if callable(func):
            def my_wrapper(*args, **kwargs):
                try:
                    ret = func(*args, **kwargs)
                except JSONRPCException as e:
                    return e.error
                else:
                    return ret
            return my_wrapper
        else:
            return func

    def blocks(self):

        reply = self.obj.getinfo()

        if 'blocks' in reply:
            return reply['blocks']

        return None

    def unlock_wallet(self, timeout=120):

        try:
            info = self.obj.walletpassphrase(self.passphrase, timeout)

            if info is None:
                return True
        except:
            pass

        return False

    def sendtoaddress(self, bitcoinaddress, amount):

        self.unlock_wallet()

        try:
            # ISSUE: should not be float, needs fix
            status = self.obj.sendtoaddress(bitcoinaddress, float(amount))
            return status
        except Exception as e:
            return error_reply(str(e))

    def validateaddress(self, bitcoinaddress):

        try:
            status = self.obj.validateaddress(bitcoinaddress)
            return status
        except Exception as e:
            return error_reply(str(e))

    def importprivkey(self, bitcoinprivkey, label='import', rescan=False):

        self.unlock_wallet()

        try:
            status = self.obj.importprivkey(bitcoinprivkey, label, rescan)
            return status
        except Exception as e:
            return error_reply(str(e))

    def format_unspents(self, unspents):
        return [{
            "transaction_hash": s["txid"],
            "output_index": s["vout"],
            "value": int(round(s["amount"]*SATOSHIS_PER_COIN)),
            "script_hex": s["scriptPubKey"],
            "confirmations": s["confirmations"]
            }
            for s in unspents
        ]

    def get_unspents(self, address):
        """ Get the spendable transaction outputs, also known as UTXOs or
            unspent transaction outputs.

            NOTE: this will only return unspents if the address provided is
            present in the bitcoind server. Use the chain, blockchain,
            or blockcypher API to grab the unspents for arbitrary addresses.
        """

        addresses = []
        addresses.append(str(address))
        min_confirmations = 0
        max_confirmation = 2000000000  # just a very large number for max

        unspents = self.obj.listunspent(min_confirmations, max_confirmation,
                                        addresses)

        return self.format_unspents(unspents)

    def broadcast_transaction(self, hex_tx):
        """ Dispatch a raw transaction to the network.
        """

        resp = self.obj.sendrawtransaction(hex_tx)
        if len(resp) > 0:
            return {'transaction_hash': resp, 'success': True}
        else:
            return error_reply('Invalid response from bitcoind.')
