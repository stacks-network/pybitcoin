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

from .utils import random_secret_exponent, random_passphrase, \
    binary_hash160, b58check_encode, b58check_decode, \
    is_hex, is_secret_exponent, is_wif_private_key
from .words import TOP_20K_ENGLISH_WORDS

class BitcoinAddress():
    _curve = ecdsa.curves.SECP256k1
    _hash_function = hashlib.sha256
    _pubkeyhash_version_byte = 0

    def _private_key_version_byte(self):
        return (self._pubkeyhash_version_byte + 128) % 256

    def __init__(self, secret_exponent=None):
        """ Takes in a private key/secret exponent as a 64-character
        hex string.
        """
        if secret_exponent:
            if not is_secret_exponent(secret_exponent):
                raise Exception("Invalid private key. Must be a 64-char hex string.")
        else:
            secret_exponent = random_secret_exponent()

        self._ecsda_private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            int(secret_exponent, 16), self._curve, self._hash_function
        )

    @classmethod
    def from_secret_exponent(cls, secret_exponent=None):
        return cls(secret_exponent)

    @classmethod
    def from_passphrase(cls, passphrase=None, num_words=12):
        """ Create address from a passphrase input (a brain wallet address)."""
        if passphrase:
            if not len(passphrase.split()) >= num_words:
                raise Exception("Warning! Passphrase must be at least " + str(num_words) + " words.")
        else:
            passphrase = random_passphrase(num_words, TOP_20K_ENGLISH_WORDS)

        # convert the passphrase to a hex private key
        hex_private_key = hashlib.sha256(passphrase).hexdigest()

        address = cls(hex_private_key)
        address._passphrase = passphrase
        return address

    @classmethod
    def from_wif(cls, wif_private_key):
        """ Create address from a wif private key. """
        if wif_private_key:
            if not is_wif_private_key(wif_private_key):
                raise Exception('Private key must be in WIF format.')
        else:
            raise Exception('A WIF private key must be provided.')

        # convert the wif private key to hex format
        hex_private_key = binascii.hexlify(b58check_decode(wif_private_key))

        return cls(hex_private_key)

    def bin_private_key(self):
        return self._ecsda_private_key.to_string()

    def hex_private_key(self):
        return binascii.hexlify(self.bin_private_key())

    def secret_exponent(self):
        """ The secret exponent *is* the private key in hex form. """
        return self.hex_private_key()

    def bin_public_key(self):
        return '\x04' + self._ecsda_private_key.get_verifying_key().to_string()

    def hex_public_key(self):
        return binascii.hexlify(self.bin_public_key())

    def bin_hash160(self):
        return binary_hash160(self.bin_public_key())

    def hex_hash160(self):
        return binascii.hexlify(self.bin_hash160())

    """ Methods with different values for different cryptocurrencies. """

    def b58check_private_key(self):
        """ Returns the private key in b58check or WIF (wallet import format) form. """
        return b58check_encode(self.bin_private_key(),
            version_byte=self._private_key_version_byte())

    def wif_private_key(self):
        return self.b58check_private_key()

    def b58check_address(self):
        return b58check_encode(self.bin_hash160(),
            version_byte=self._pubkeyhash_version_byte)

    def __str__(self):
        return self.b58check_address()

    """ Brain wallet address methods """

    def passphrase(self):
        if hasattr(self, '_passphrase'):
            return self._passphrase
        else:
            raise Exception("No passphrase! This isn't a brain wallet address!")

class LitecoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 48

class NamecoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 52

class PeercoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 55

class PrimecoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 23

class DogecoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 30

class WorldcoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 73

class FeathercoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 14

class TerracoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 0

class NovacoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 8

class IxcoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 138

class TestnetAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 111

class ProtosharesAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 56

class MemorycoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 50

class QuarkcoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 58

class InfinitecoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 102

class CryptogenicbullionAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 11

class AnoncoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 23

class MegacoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 50

class EarthcoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 93

class NetcoinAddress(BitcoinAddress):
    _pubkeyhash_version_byte = 112



