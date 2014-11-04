# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from binascii import hexlify, unhexlify
import struct
from .utils import flip_endian, variable_length_int, UINT_MAX

def serialize_input(input, signature_script_hex=''):
    """ Serializes a transaction input.
    """
    if not (isinstance(input, dict) and 'transaction_hash' in input \
            and 'output_index' in input):
        raise Exception('Required parameters: transaction_hash, output_index')

    if not 'sequence' in input:
        input['sequence'] = UINT_MAX

    return ''.join([
        flip_endian(input['transaction_hash']),
        hexlify(struct.pack('<I', input['output_index'])),
        hexlify(variable_length_int(len(signature_script_hex)/2)),
        signature_script_hex,
        hexlify(struct.pack('<I', input['sequence']))
    ])

def serialize_output(output):
    """ Serializes a transaction output.
    """
    if not ('value' in output and 'script_hex' in output):
        raise Exception('Invalid output')

    return ''.join([
        hexlify(struct.pack('<Q', output['value'])), # pack into 8 bites
        hexlify(variable_length_int(len(output['script_hex'])/2)),
        output['script_hex']
    ])

def serialize_transaction(inputs, outputs, lock_time=0, version=1):
    """ Serializes a transaction.
    """

    # add in the inputs
    serialized_inputs = ''.join([serialize_input(input) for input in inputs])

    # add in the outputs
    serialized_outputs = ''.join([serialize_output(output) for output in outputs])

    return ''.join([
        # add in the version number
        hexlify(struct.pack('<I', version)),
        # add in the number of inputs
        hexlify(variable_length_int(len(inputs))),
        # add in the inputs
        serialized_inputs,
        # add in the number of outputs
        hexlify(variable_length_int(len(outputs))),
        # add in the outputs
        serialized_outputs,
        # add in the lock time
        hexlify(struct.pack('<I', lock_time)),
    ])

from .scripts import make_pay_to_address_script
from .utils import STANDARD_FEE

def make_pay_to_address_transaction(inputs, to_address, change_address,
        send_amount, fee=STANDARD_FEE):
    """ Takes in inputs, a recipient address, and a send amount (in satoshis)
        and builds an unsigned transaction.
    """
    # calculate the total amount  coming into the transaction from the inputs
    total_amount_in = sum([input['value'] for input in inputs])
    # change = whatever is left over from the amount sent & the transaction fee
    change_amount = total_amount_in - send_amount - fee

    if change_amount < 0:
        raise Exception('Not enough inputs for transaction.')

    # put together the list of transaction outputs
    outputs = [
        # the output that sends money to the recipient
        { "script_hex": make_pay_to_address_script(to_address),
          "value": send_amount },
        # the output that send the leftover change to the change address
        { "script_hex": make_pay_to_address_script(change_address),
          "value": change_amount }
    ]
    # return the serialized transaction
    return serialize_transaction(inputs, outputs)

