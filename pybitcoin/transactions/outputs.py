# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .scripts import make_pay_to_address_script, make_op_return_script
from ..constants import STANDARD_FEE, OP_RETURN_FEE

def calculate_change_amount(inputs, send_amount, fee):
    # calculate the total amount  coming into the transaction from the inputs
    total_amount_in = sum([input['value'] for input in inputs])
    # change = whatever is left over from the amount sent & the transaction fee
    change_amount = total_amount_in - send_amount - fee
    # check to ensure the change amount is a non-negative value and return it
    if change_amount < 0:
        raise ValueError('Not enough inputs for transaction (total: %s, to spend: %s, fee: %s).' % (total_amount_in, send_amount, fee))
    return change_amount

def make_pay_to_address_outputs(to_address, send_amount, inputs, change_address,
                                fee=STANDARD_FEE):
    """ Builds the outputs for a "pay to address" transaction.
    """
    return [
        # main output
        { "script_hex": make_pay_to_address_script(to_address), "value": send_amount },
        # change output
        { "script_hex": make_pay_to_address_script(change_address),
          "value": calculate_change_amount(inputs, send_amount, fee)
        }
    ]

def make_op_return_outputs(data, inputs, change_address, fee=OP_RETURN_FEE,
                           send_amount=0, format='bin'):
    """ Builds the outputs for an OP_RETURN transaction.
    """
    return [
        # main output
        { "script_hex": make_op_return_script(data, format=format), "value": send_amount },
        # change output
        { "script_hex": make_pay_to_address_script(change_address),
          "value": calculate_change_amount(inputs, send_amount, fee)
        }
    ]
