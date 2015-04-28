# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import json
import hashlib
import ecdsa
from binascii import hexlify, unhexlify
from ecdsa.keys import SigningKey
from utilitybelt import is_int, dev_random_entropy, dev_urandom_entropy
from pybitcointools import compress

from .errors import _errors
from .formatcheck import *
from .b58check import b58check_encode, b58check_decode
from .publickey import BitcoinPublicKey, PUBKEY_MAGIC_BYTE
from .passphrases import create_passphrase


def random_secret_exponent(curve_order):
    """ Generates a random secret exponent. """
    # run a rejection sampling algorithm to ensure the random int is less
    # than the curve order
    while True:
        # generate a random 256 bit hex string
        random_hex = hexlify(dev_random_entropy(32))
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            break
    return random_int


class BitcoinPrivateKey():
    _curve = ecdsa.curves.SECP256k1
    _hash_function = hashlib.sha256
    _pubkeyhash_version_byte = 0

    @classmethod
    def wif_version_byte(cls):
        if hasattr(cls, '_wif_version_byte'):
            return cls._wif_version_byte
        return (cls._pubkeyhash_version_byte + 128) % 256

    def __init__(self, private_key=None):
        """ Takes in a private key/secret exponent.
        """
        if not private_key:
            secret_exponent = random_secret_exponent(self._curve.order)
        else:
            private_key = str(private_key)

            if is_int(private_key):
                secret_exponent = private_key
            elif is_256bit_hex_string(private_key):
                secret_exponent = int(private_key, 16)
            elif is_wif_pk(private_key):
                secret_exponent = int(
                    hexlify(b58check_decode(private_key)), 16)
            else:
                raise Exception('Not a valid private key format.')

        # make sure that: 1 <= secret_exponent < curve_order
        if not is_secret_exponent(secret_exponent, self._curve.order):
            raise IndexError(_errors["EXPONENT_OUTSIDE_CURVE_ORDER"])

        self._ecdsa_private_key = ecdsa.keys.SigningKey.from_secret_exponent(
            secret_exponent, self._curve, self._hash_function
        )

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
                raise ValueError(_errors["CURVE_ORDER_EXCEEDED"])

        keypair = cls(hex_private_key)
        keypair._passphrase = passphrase
        return keypair

    def to_bin(self):
        return self._ecdsa_private_key.to_string()

    def to_hex(self):
        return hexlify(self.to_bin())

    def to_wif(self):
        return b58check_encode(
            self.to_bin(), version_byte=self.wif_version_byte())

    def to_pem(self):
        return self._ecdsa_private_key.to_pem()

    def public_key(self, compressed=False):
        # lazily calculate and set the public key
        if not hasattr(self, '_public_key'):
            ecdsa_public_key = self._ecdsa_private_key.get_verifying_key()

            # compress the public key string if a compressed public key is
            # desired
            bin_public_key_string = PUBKEY_MAGIC_BYTE + \
                ecdsa_public_key.to_string()
            if compressed:
                bin_public_key_string = compress(bin_public_key_string)
            # create the public key object from the public key string
            self._public_key = BitcoinPublicKey(
                bin_public_key_string,
                version_byte=self._pubkeyhash_version_byte)

        # return the public key object
        return self._public_key

    def passphrase(self):
        if hasattr(self, '_passphrase'):
            return self._passphrase
        else:
            raise Exception(_errors["NOT_A_BRAIN_WALLET"])


class LitecoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 48


class NamecoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 52
