# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~
    
    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import json
import ecdsa
import hashlib
import binascii

from .utils import random_secret_exponent, is_hex, binary_hash160, \
    base58check_encode, random_passphrase
from .words import TOP_20K_ENGLISH_WORDS

class BitcoinWallet():
    _curve = ecdsa.curves.SECP256k1
    _hash_function = hashlib.sha256
    _version_bytes = {
        'pubkey_hash': 0,
        'private_key': 0+128,
    }

    def __init__(self, hex_private_key=None):
        """ Takes in a private key/secret exponent as a 64-character
        hex string.
        """
        if not hex_private_key:
            hex_private_key = random_secret_exponent()

        if not (len(hex_private_key) == 64 and is_hex(hex_private_key)):
            raise Exception("Invalid private key. Must be a 64-char hex string.")

        self.private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            int(hex_private_key, 16), self._curve, self._hash_function
        )

    def bin_private_key(self):
        return self.private_key.to_string()

    def hex_private_key(self):
        return binascii.hexlify(self.bin_private_key())

    def hex_secret_exponent(self):
        """ The secret exponent *is* the private key in hex form. """
        return self.hex_private_key()

    def bin_public_key(self):
        return '\x04' + self.private_key.get_verifying_key().to_string()

    def hex_public_key(self):
        return binascii.hexlify(self.bin_public_key())

    def bin_hash160(self):
        return binary_hash160(self.bin_public_key())

    def hex_hash160(self):
        return binascii.hexlify(self.bin_hash160())

    """ Methods with different values for different cryptocurrencies. """

    def wif_private_key(self):
        return base58check_encode(self.bin_private_key(),
            version_byte=self._version_bytes['private_key'])

    def address(self):
        return base58check_encode(self.bin_hash160(),
            version_byte=self._version_bytes['pubkey_hash'])

    """ BrainWallet methods """

    @classmethod
    def from_passphrase(cls, passphrase=None):
        """ Create wallet from a passphrase input (a brain wallet)."""
        PHRASE_LENGTH = 12

        if not passphrase:
            passphrase = random_passphrase(PHRASE_LENGTH, TOP_20K_ENGLISH_WORDS)
        
        if not (passphrase and len(passphrase.split()) >= PHRASE_LENGTH):
            raise Exception("Passphrase must be at least 12 words.")

        hex_private_key = hashlib.sha256(passphrase).hexdigest()

        wallet = cls(hex_private_key)
        wallet._passphrase = passphrase
        return wallet

    def passphrase(self):
        if hasattr(self, '_passphrase'):
            return self._passphrase
        else:
            raise Exception("No passphrase! This isn't a brain wallet!")

class LitecoinWallet(BitcoinWallet):
    _version_bytes = {
        'pubkey_hash': 48,
        'private_key': 48+128,
    }

class NamecoinWallet(BitcoinWallet):
    _version_bytes = {
        'pubkey_hash': 52,
        'private_key': 52+128,
    }

class PeercoinWallet(BitcoinWallet):
    _version_bytes = {
        'pubkey_hash': 55,
        'private_key': 55+128,
    }

class PrimecoinWallet(BitcoinWallet):
    _version_bytes = {
        'pubkey_hash': 23,
        'private_key': 23+128,
    }

