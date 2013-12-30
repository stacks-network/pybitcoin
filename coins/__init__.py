# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~

    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1.8'

from .addresses import BitcoinAddress, LitecoinAddress, NamecoinAddress, \
    PeercoinAddress, PrimecoinAddress
from .utils import random_secret_exponent, random_passphrase, \
    b58check_encode, b58check_decode, b58check_unpack, b58check_version_byte, \
    is_hex, is_valid_b58check, is_hex_private_key, is_wif_private_key

