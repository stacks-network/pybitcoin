# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~
    
    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os, json, binascii, hashlib, ecdsa
from ecdsa.keys import VerifyingKey

from .errors import _errors
from .hash160 import Hash160, bin_hash160
from .formatcheck import *

class BitcoinPublicKey():
    _curve = ecdsa.curves.SECP256k1
    _hash_function = hashlib.sha256
    _version_byte = 0

    @classmethod
    def version_byte(cls):
        return cls._version_byte

    def __init__(self, public_key, version_byte=0):
        """ Takes in a public key in hex format.
        """
        self._version_byte = version_byte

        if is_hex(public_key) and public_key[0:2] == '04':
            public_key = public_key[2:]
        elif public_key[0] == '\x04':
            public_key = public_key[1:]

        if is_hex_ecdsa_pubkey(public_key):
            bin_public_key = binascii.unhexlify(public_key)
        elif is_binary_ecdsa_pubkey(public_key):
            bin_public_key = public_key
        else:
            raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])
        
        try:
            self._ecdsa_public_key = VerifyingKey.from_string(
                bin_public_key, self._curve)
        except AssertionError as e:
            raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])
        
        self._hash160 = Hash160(self.to_bin(prefix=True), self._version_byte)

    def to_bin(self, prefix=True):
        ecdsa_public_key = self._ecdsa_public_key.to_string()
        if prefix:
            return '\x04' + ecdsa_public_key
        return ecdsa_public_key

    def to_hex(self, prefix=True):
        return binascii.hexlify(self.to_bin(prefix=prefix))

    def hash160(self):
        return self._hash160.to_hex()

    def bin_hash160(self):
        return self._hash160.to_bin()

    def address(self):
        """ The address is the hash160 in b58check format. """
        return self._hash160.address()

class LitecoinPublicKey(BitcoinPublicKey):
    _version_byte = 48

class NamecoinPublicKey(BitcoinPublicKey):
    _version_byte = 52

