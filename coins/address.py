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

from .utils import random_secret_exponent, random_256bit_passphrase, \
    random_160bit_passphrase, \
    binary_hash160, b58check_encode, b58check_decode, \
    is_hex, is_secret_exponent, is_wif_private_key

class BitcoinAddress():
    _curve = ecdsa.curves.SECP256k1
    _hash_function = hashlib.sha256
    _pubkeyhash_version_byte = 0

    @classmethod
    def version_byte(cls, type='pubkey_hash'):
        if type == 'pubkey_hash':
            return cls._pubkeyhash_version_byte
        elif type == 'private_key':
            return (cls._pubkeyhash_version_byte + 128) % 256
        else:
            raise Exception("type must be 'pubkey_hash' or 'privatekey'")

    def __init__(self, secret_exponent=None):
        """ Takes in a private key/secret exponent as a 64-character
        hex string.
        """
        if secret_exponent:
            if is_secret_exponent(secret_exponent):
                secret_exponent = int(secret_exponent, 16)
            else:
                raise Exception("Invalid private key. Must be a 64-char hex string.")
        else:
            secret_exponent = int(random_secret_exponent(), 16)

        # make sure that: 1 < secret_exponent < curve_order
        if secret_exponent > self._curve.order:
            secret_exponent = secret_exponent - self._curve.order
        elif secret_exponent == self._curve.order:
            secret_exponent = 1

        self._ecsda_private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, self._curve, self._hash_function
        )

    @classmethod
    def from_secret_exponent(cls, secret_exponent=None):
        return cls(secret_exponent)

    @classmethod
    def from_passphrase(cls, passphrase=None, min_words=12, bits_of_entropy=160):
        """ Create address from a passphrase input (a brain wallet address)."""
        if passphrase:
            if not len(passphrase.split()) >= min_words:
                raise Exception("Warning! Passphrase must be at least " + str(min_words) + " words.")
        else:
            if bits_of_entropy == 160:
                passphrase = random_160bit_passphrase()
            elif bits_of_entropy == 256:
                passphrase = random_256bit_passphrase()
            else:
                raise Exception("'bits_of_entropy' must be 160 or 256")

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
            raise Exception("A WIF private key must be provided.")

        # convert the wif private key to hex format
        hex_private_key = binascii.hexlify(b58check_decode(wif_private_key))

        return cls(hex_private_key)

    def _bin_private_key(self):
        return self._ecsda_private_key.to_string()

    def _bin_public_key(self):
        return '\x04' + self._ecsda_private_key.get_verifying_key().to_string()

    def _bin_hash160(self):
        return binary_hash160(self._bin_public_key())

    def private_key(self, format='wif'):
        if format == 'bin':
            return self._bin_private_key()
        elif format == 'hex':
            return binascii.hexlify(self._bin_private_key())
        elif format == 'wif' or format == 'b58check':
            return b58check_encode(self._bin_private_key(),
                version_byte=self.version_byte('private_key'))
        else:
            raise Exception("format must be 'bin', 'hex', 'wif', or 'b58check.")

    def public_key(self, format='hex'):
        if format == 'bin':
            return self._bin_public_key()
        elif format == 'hex':
            return binascii.hexlify(self._bin_public_key())
        else:
            raise Exception("format must be 'bin' or 'hex'.")

    def hash160(self, format='hex'):
        if format == 'bin':
            return self._bin_hash160()
        elif format == 'hex':
            return binascii.hexlify(self._bin_hash160())
        elif format == 'b58check':
            return b58check_encode(self._bin_hash160(),
                version_byte=self.version_byte('pubkey_hash'))
        else:
            raise Exception("format must be 'bin', 'hex', or 'b58check.")

    def secret_exponent(self):
        """ The secret exponent *is* the private key in hex form. """
        return self.private_key('hex')

    def wif(self):
        """ The secret exponent *is* the private key in hex form. """
        return self.private_key('wif')

    def __str__(self):
        """ The address *is* the hash160 in b58check format. """
        return self.hash160('b58check')

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



