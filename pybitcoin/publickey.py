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
from ecdsa.keys import VerifyingKey
from bitcoin import decompress, compress, pubkey_to_address
from utilitybelt import is_hex

from .errors import _errors
from .hash import bin_hash160 as get_bin_hash160
from .formatcheck import is_hex_ecdsa_pubkey, is_binary_ecdsa_pubkey
from .b58check import b58check_encode
from .address import bin_hash160_to_address

PUBKEY_MAGIC_BYTE = '\x04'


class CharEncoding():
    hex = 16
    bin = 256


class PubkeyType():
    ecdsa = 1
    uncompressed = 2
    compressed = 3


def get_public_key_format(public_key_string):
    if not isinstance(public_key_string, str):
        raise ValueError('Public key must be a string.')

    if len(public_key_string) == 64:
        return CharEncoding.bin, PubkeyType.ecdsa

    if (len(public_key_string) == 65 and
            public_key_string[0] == PUBKEY_MAGIC_BYTE):
        return CharEncoding.bin, PubkeyType.uncompressed

    if len(public_key_string) == 33:
        return CharEncoding.bin, PubkeyType.compressed

    if is_hex(public_key_string):
        if len(public_key_string) == 128:
            return CharEncoding.hex, PubkeyType.ecdsa

        if (len(public_key_string) == 130 and
                public_key_string[0:2] == hexlify(PUBKEY_MAGIC_BYTE)):
            return CharEncoding.hex, PubkeyType.uncompressed

        if len(public_key_string) == 66:
            return CharEncoding.hex, PubkeyType.compressed

    raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])


def extract_bin_ecdsa_pubkey(public_key):
    key_charencoding, key_type = get_public_key_format(public_key)

    if key_charencoding == CharEncoding.hex:
        bin_public_key = unhexlify(public_key)
    elif key_charencoding == CharEncoding.bin:
        bin_public_key = public_key
    else:
        raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])

    if key_type == PubkeyType.ecdsa:
        return bin_public_key
    elif key_type == PubkeyType.uncompressed:
        return bin_public_key[1:]
    elif key_type == PubkeyType.compressed:
        return decompress(bin_public_key)[1:]
    else:
        raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])


def extract_bin_bitcoin_pubkey(public_key):
    key_charencoding, key_type = get_public_key_format(public_key)

    if key_charencoding == CharEncoding.hex:
        bin_public_key = unhexlify(public_key)
    elif key_charencoding == CharEncoding.bin:
        bin_public_key = public_key
    else:
        raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])

    if key_type == PubkeyType.ecdsa:
        return PUBKEY_MAGIC_BYTE + bin_public_key
    elif key_type == PubkeyType.uncompressed:
        return bin_public_key
    elif key_type == PubkeyType.compressed:
        return bin_public_key
    else:
        raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])


class BitcoinPublicKey():
    _curve = ecdsa.curves.SECP256k1
    _version_byte = 0

    @classmethod
    def version_byte(cls):
        return cls._version_byte

    def __init__(self, public_key_string, version_byte=None, verify=True):
        """ Takes in a public key in hex format.
        """
        # set the version byte
        if version_byte:
            self._version_byte = version_byte

        self._charencoding, self._type = get_public_key_format(
            public_key_string)

        # extract the binary bitcoin key (compressed/uncompressed w magic byte)
        self._bin_public_key = extract_bin_bitcoin_pubkey(public_key_string)

        # extract the bin ecdsa public key (uncompressed, w/out a magic byte)
        bin_ecdsa_public_key = extract_bin_ecdsa_pubkey(public_key_string)
        if verify:
            try:
                # create the ecdsa key object
                self._ecdsa_public_key = VerifyingKey.from_string(
                    bin_ecdsa_public_key, self._curve)
            except AssertionError as e:
                raise ValueError(_errors['IMPROPER_PUBLIC_KEY_FORMAT'])

    def to_bin(self):
        return self._bin_public_key

    def to_hex(self):
        return hexlify(self.to_bin())

    def to_pem(self):
        return self._ecdsa_public_key.to_pem()

    def to_der(self):
        return hexlify(self._ecdsa_public_key.to_der())

    def bin_hash160(self):
        if not hasattr(self, '_bin_hash160'):
            self._bin_hash160 = get_bin_hash160(self.to_bin())
        return self._bin_hash160

    def hash160(self):
        return hexlify(self.bin_hash160())

    def address(self):
        if self._type == PubkeyType.compressed:
            bin_hash160 = get_bin_hash160(compress(self.to_bin()))
            return bin_hash160_to_address(
                bin_hash160, version_byte=self._version_byte)

        return bin_hash160_to_address(self.bin_hash160(),
                                      version_byte=self._version_byte)


class LitecoinPublicKey(BitcoinPublicKey):
    _version_byte = 48


class NamecoinPublicKey(BitcoinPublicKey):
    _version_byte = 52
