# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .opcodes import *
from ..b58check import b58check_decode
from binascii import hexlify

def make_pay_to_address_script(address):
    """ Takes in an address and returns the script 
    """
    hash160 = hexlify(b58check_decode(address))
    bytes_to_push = len(hash160)/2
    return '%x%x%x%s%x%x' % (OP_DUP, OP_HASH160, bytes_to_push, hash160,
        OP_EQUALVERIFY, OP_CHECKSIG)
