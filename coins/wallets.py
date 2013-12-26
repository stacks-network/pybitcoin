# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~
    
    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json
import ecdsa
import hashlib
import binascii
from utils import random_secret_exponent, is_hex, binary_hash160, \
    base58check_encode, random_passphrase

WORD_LIST_FILENAME = 'coins/data/top_20k_english_words.json'
with open(WORD_LIST_FILENAME, 'r') as f:
    TOP_20K_ENGLISH_WORDS = json.loads(f.read())

class BitcoinWallet():
    curve = ecdsa.curves.SECP256k1
    hash_function = hashlib.sha256
    version_bytes = {
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
            raise Exception('Invalid private key. Must be a 64-char hex string.')

        self.private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            int(hex_private_key, 16), self.curve, self.hash_function
        )

    @classmethod
    def from_passphrase(cls, passphrase=None):
        """ Create wallet from a passphrase input (a brain wallet)."""
        if not passphrase:
            passphrase = random_passphrase(12, TOP_20K_ENGLISH_WORDS)
        
        if not (passphrase and len(passphrase.split()) >= 12):
            raise Exception('Passphrase must be at least 12 words.')

        hex_private_key = hashlib.sha256(passphrase).hexdigest()

        b = cls(hex_private_key)
        b.passphrase = passphrase
        return b

    def bin_private_key(self):
        return self.private_key.to_string()

    def hex_private_key(self):
        return binascii.hexlify(self.bin_private_key())

    def hex_secret_exponent(self):
        return self.hex_private_key()

    def bin_public_key(self):
        return '\x04' + self.private_key.get_verifying_key().to_string()

    def hex_public_key(self):
        return binascii.hexlify(self.bin_public_key())

    def bin_hash160(self):
        return binary_hash160(self.bin_public_key())

    def hex_hash160(self):
        return binascii.hexlify(self.bin_hash160())

    def wif_private_key(self):
        return base58check_encode(self.bin_private_key(),
            version_byte=self.version_bytes['private_key'])

    def address(self):
        return base58check_encode(self.bin_hash160(),
            version_byte=self.version_bytes['pubkey_hash'])

class LitecoinWallet(BitcoinWallet):
    version_bytes = {
        'pubkey_hash': 48,
        'private_key': 48+128,
    }

class NamecoinWallet(BitcoinWallet):
    version_bytes = {
        'pubkey_hash': 52,
        'private_key': 52+128,
    }

class PeercoinWallet(BitcoinWallet):
    version_bytes = {
        'pubkey_hash': 55,
        'private_key': 55+128,
    }

class PrimecoinWallet(BitcoinWallet):
    version_bytes = {
        'pubkey_hash': 23,
        'private_key': 23+128,
    }

