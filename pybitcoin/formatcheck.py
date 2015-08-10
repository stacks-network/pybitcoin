# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import re
import random
import binascii
from utilitybelt import is_int, is_hex

from .b58check import is_b58check


def is_secret_exponent(val, curve_order):
    return (isinstance(val, (int, long)) and val >= 1 and val < curve_order)


def is_256bit_hex_string(val):
    return (isinstance(val, str) and len(val) == 64 and is_hex(val))


def is_wif_pk(val):
    return (len(val) >= 51 and len(val) <= 52 and is_b58check(val))


def is_b58check_address(val):
    return is_b58check(val)
    # return (len(val) >= 27 and len(val) <= 34 and is_b58check(val))


def is_hex_ecdsa_pubkey(val):
    return (is_hex(val) and len(val) == 128)


def is_binary_ecdsa_pubkey(val):
    return (isinstance(val, str) and len(val) == 64)
