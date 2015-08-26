# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

from binascii import unhexlify, hexlify
from .b58check import b58check_encode, b58check_decode


def bin_hash160_to_address(bin_hash160, version_byte=0):
    return b58check_encode(bin_hash160, version_byte=version_byte)


def hex_hash160_to_address(hash160, version_byte=0):
    return bin_hash160_to_address(
        unhexlify(hash160), version_byte=version_byte)


def script_hex_to_address(script, version_byte=0):
    if script[0:6] == '76a914' and script[-4:] == '88ac':
        bin_hash160 = unhexlify(script[6:-4])
        return bin_hash160_to_address(bin_hash160, version_byte=version_byte)
    return None


def address_to_bin_hash160(address):
    return b58check_decode(address)


def address_to_hex_hash160(address):
    return hexlify(address_to_bin_hash160(address))


def address_to_new_cryptocurrency(address, new_version_number):
    bin_hash160 = address_to_bin_hash160(address)
    return bin_hash160_to_address(bin_hash160, new_version_number)
