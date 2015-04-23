# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import json
import binascii
import ecdsa
import hashlib

from .privatekey import random_secret_exponent
from .b58check import b58check_encode, b58check_decode, b58check_unpack, \
    b58check_version_byte
from .errors import _errors
from .hash import bin_hash160
from .formatcheck import is_int, is_256bit_hex_string, is_wif_pk, \
    is_secret_exponent
from .passphrases import create_passphrase


class BitcoinKeypair():
    """ NOTE: This object has been replaced by the BitcoinPrivateKey and 
        BitcoinPublicKey objects and is set to be deprecated at a future date.
    """

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
        if not private_key:
            secret_exponent = random_secret_exponent(self._curve.order)
        elif is_int(private_key):
            secret_exponent = private_key
        elif is_256bit_hex_string(private_key):
            secret_exponent = int(private_key, 16)
        elif is_wif_pk(private_key):
            secret_exponent = int(
                binascii.hexlify(b58check_decode(private_key)), 16)

        # make sure that: 1 <= secret_exponent < curve_order
        if not is_secret_exponent(secret_exponent, self._curve.order):
            raise IndexError(_errors["EXPONENT_OUTSIDE_CURVE_ORDER"])

        self._ecdsa_private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, self._curve, self._hash_function
        )
        self._ecdsa_public_key = self._ecdsa_private_key.get_verifying_key()

    @classmethod
    def from_private_key(cls, private_key=None):
        return cls(private_key)

    @classmethod
    def from_passphrase(cls, passphrase=None):
        """ Create keypair from a passphrase input (a brain wallet keypair)."""
        if not passphrase:
            # run a rejection sampling algorithm to ensure the private key is
            # less than the curve order
            while True:
                passphrase = create_passphrase(bits_of_entropy=160)
                hex_private_key = hashlib.sha256(passphrase).hexdigest()
                if int(hex_private_key, 16) < cls._curve.order:
                    break
        else:
            hex_private_key = hashlib.sha256(passphrase).hexdigest()
            if not (int(hex_private_key, 16) < cls._curve.order):
                raise ValueError(_errors["PHRASE_YIELDS_INVALID_EXPONENT"])

        keypair = cls(hex_private_key)
        keypair._passphrase = passphrase
        return keypair

    def _bin_private_key(self):
        return self._ecdsa_private_key.to_string()

    def _bin_public_key(self, prefix=True):
        ecdsa_public_key = self._ecdsa_public_key.to_string()
        if prefix:
            return '\x04' + ecdsa_public_key
        return ecdsa_public_key

    def _bin_hash160(self):
        return bin_hash160(self._bin_public_key())

    def private_key(self, format='hex'):
        if format == 'bin':
            return self._bin_private_key()
        elif format == 'hex':
            return binascii.hexlify(self._bin_private_key())
        elif format == 'wif' or format == 'b58check':
            return b58check_encode(
                self._bin_private_key(),
                version_byte=self.version_byte('private_key'))
        else:
            raise ValueError(_errors["MUST_BE_VALID_PRIVKEY_FORMAT"])

    def public_key(self, format='hex'):
        if format == 'bin':
            return self._bin_public_key()
        elif format == 'hex':
            return binascii.hexlify(self._bin_public_key())
        else:
            raise ValueError(_errors["MUST_BE_VALID_PUBKEY_FORMAT"])

    def hash160(self, format='hex'):
        if format == 'bin':
            return self._bin_hash160()
        elif format == 'hex':
            return binascii.hexlify(self._bin_hash160())
        elif format == 'b58check':
            return b58check_encode(
                self._bin_hash160(),
                version_byte=self.version_byte('pubkey_hash'))
        else:
            raise ValueError(_errors["MUST_BE_VALID_HASH160_FORMAT"])

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
            raise Exception(_errors["NOT_A_BRAIN_WALLET"])


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


class HuntercoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 40


class VertcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 71


class ReddcoinKeypair(BitcoinKeypair):
    _pubkeyhash_version_byte = 61

# TO DO:
# auroracoin
# counterparty
# darkcoin
# ybcoin
# maxcoin
# mintcoin
# devcoin
# tickets
# freicoin
# zetacoin
# digitalcoin
# copperlark
# applecoin
# unobtanium
# fedoracoin
# cachecoin
# mincoin
# ultracoin
# colossuscoin
# blackcoin
# securecoin
# gridcoin
# billioncoin
# kittehcoin
# karmacoin
# mooncoin
# sexcoin
