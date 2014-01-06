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

from .utils import random_secret_exponent, random_160bit_passphrase
from .utils import  binary_hash160, b58check_encode, b58check_decode, \
    b58check_unpack, b58check_version_byte
from .utils import is_hex, is_valid_secret_exponent, is_256bit_hex_string, \
    is_wallet_import_format, is_valid_b58check_address, extract_pk_as_int

class BitcoinKeypair():
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

    def __init__(self, private_key=None):
        """ Takes in a private key/secret exponent.
        """
        if private_key:
            secret_exponent = extract_pk_as_int(private_key, self._curve.order)
        else:
            secret_exponent = random_secret_exponent(self._curve.order)
        
        self._ecsda_private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, self._curve, self._hash_function
        )

    @classmethod
    def from_private_key(cls, private_key=None):
        return cls(private_key)

    @classmethod
    def from_passphrase(cls, passphrase=None, min_words=12):
        """ Create keypair from a passphrase input (a brain wallet keypair)."""
        if passphrase:
            if not len(passphrase.split()) >= min_words:
                raise Exception("Warning! Passphrase must be at least " + str(min_words) + " words.")
        else:
            passphrase = random_160bit_passphrase()

        # convert the passphrase to a hex private key
        hex_private_key = hashlib.sha256(passphrase).hexdigest()

        keypair = cls(hex_private_key)
        keypair._passphrase = passphrase
        return keypair

    def _bin_private_key(self):
        return self._ecsda_private_key.to_string()

    def _bin_public_key(self):
        return '\x04' + self._ecsda_private_key.get_verifying_key().to_string()

    def _bin_hash160(self):
        return binary_hash160(self._bin_public_key())

    def private_key(self, format='hex'):
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
        """ The secret exponent is the private key in int or hex format. """
        return self.private_key('hex')

    def wif_pk(self):
        """ The "wif pk" is the private key in wallet import format. """
        return self.private_key('wif')

    def address(self):
        """ The address is the hash160 in b58check format. """
        return self.hash160('b58check')

    """ Brain wallet address methods """

    def passphrase(self):
        if hasattr(self, '_passphrase'):
            return self._passphrase
        else:
            raise Exception("No passphrase! This isn't a brain wallet address!")

class LitecoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 48

class NamecoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 52

class PeercoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 55

class PrimecoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 23

class DogecoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 30

class WorldcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 73

class FeathercoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 14

class TerracoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 0

class NovacoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 8

class IxcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 138

class TestnetKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 111

class ProtosharesKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 56

class MemorycoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 50

class QuarkcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 58

class InfinitecoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 102

class CryptogenicbullionKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 11

class AnoncoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 23

class MegacoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 50

class EarthcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 93

class NetcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 112



