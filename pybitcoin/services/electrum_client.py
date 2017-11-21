"""
Electrum client for pybitcoin
"""

import jsonrpclib

from ..transactions.serialize import deserialize_transaction


class ElectrumClient():
    """
    Electrum Blockchain interface class
    """
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.electrum = jsonrpclib.Server(self.api_endpoint)

    def _format_unspents(self, unspents):
        """
        Make electrum's output consumable by pybitcoin.
        """
        # FIXME: This is off-by-one and behavior for unconfirmed is unknown,
        # will leave out for now.
        # daemon_status = self.electrum.daemon({'subcommand': 'status'})
        # blockchain_height = daemon_status['blockchain_height']
        formatted_unspents = []
        for unspent in unspents:
            tx_hash = unspent['tx_hash']
            transaction = self.electrum.gettransaction(tx_hash)['hex']
            deserialized_tx = deserialize_transaction(transaction)
            script_hex = deserialized_tx[1][0]['script_hex']
            # confirmations = blockchain_height - unspent['height']
            confirmations = 0
            # electrum's tx_hash is the big endian version already.
            formatted_unspent = {'transaction_hash': unspent['tx_hash'],
                                 'output_index': unspent['tx_pos'],
                                 'value': unspent['value'],
                                 'script_hex': script_hex,
                                 'confirmations': confirmations}
            formatted_unspents.append(formatted_unspent)
        return formatted_unspents

    def get_unspents(self, address):
        unspents = self.electrum.getaddressunspent(address)
        return self._format_unspents(unspents)

    def broadcast_transaction(self, tx):
        broadcast_output = self.electrum.broadcast(tx)
        if broadcast_output[0] is False:
            raise Exception(str(broadcast_output))
        else:
            return broadcast_output
