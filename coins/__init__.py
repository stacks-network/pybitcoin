# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~

    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.2.0'

from .keypair import *

from .utils import random_secret_exponent, random_256bit_passphrase, \
    random_160bit_passphrase
from .utils import  binary_hash160, b58check_encode, b58check_decode, \
    b58check_unpack, b58check_version_byte
from .utils import is_hex, is_valid_secret_exponent, is_256bit_hex_string, \
    is_wallet_import_format, is_valid_b58check_address, extract_pk_as_int

