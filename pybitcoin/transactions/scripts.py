# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from .opcodes import *
from .utils import count_bytes
from ..constants import MAX_BYTES_AFTER_OP_RETURN
from ..b58check import b58check_decode, b58check_encode
from binascii import hexlify, unhexlify
from utilitybelt import is_hex

def script_to_hex(script):
    """ Parse the string representation of a script and return the hex version.
        Example: "OP_DUP OP_HASH160 c629...a6db OP_EQUALVERIFY OP_CHECKSIG"
    """
    hex_script = ''
    parts = script.split(' ')
    for part in parts:
        if part[0:3] == 'OP_':
            try:
                hex_script += '%0.2x' % eval(part)
            except:
                raise Exception('Invalid opcode: %s' % part)
        elif isinstance(part, (int)):
            hex_script += '%0.2x' % part
        elif is_hex(part):
            hex_script += '%0.2x' % count_bytes(part) + part
        else:
            raise Exception('Invalid script - only opcodes and hex characters allowed.')
    return hex_script

def make_pay_to_address_script(address):
    """ Takes in an address and returns the script 
    """
    hash160 = hexlify(b58check_decode(address))
    script_string = 'OP_DUP OP_HASH160 %s OP_EQUALVERIFY OP_CHECKSIG' % hash160
    return script_to_hex(script_string)

def make_op_return_script(data, format='bin'):
    """ Takes in raw ascii data to be embedded and returns a script.
    """
    if format == 'hex':
        assert(is_hex(data))
        hex_data = data
    elif format == 'bin':
        hex_data = hexlify(data)
    else:
        raise Exception("Format must be either 'hex' or 'bin'")

    num_bytes = count_bytes(hex_data)
    if num_bytes > MAX_BYTES_AFTER_OP_RETURN:
        raise Exception('Data is %i bytes - must not exceed 40.' % num_bytes)

    script_string = 'OP_RETURN %s' % hex_data
    return script_to_hex(script_string)

