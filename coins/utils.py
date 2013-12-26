# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~
    
    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import re
import random
import hashlib
import binascii

def dev_random_entropy(numbytes):
    return open("/dev/random", "rb").read(numbytes)

def dev_urandom_entropy(numbytes):
    return open("/dev/urandom", "rb").read(numbytes)

def random_secret_exponent():
    """ Generates a random secret exponent and returns it as a hex string. """
    return binascii.hexlify(dev_random_entropy(32))

def is_hex(string):
    try:
        int(string, 16)
    except ValueError:
        return False
    else:
        return True

def int_to_hex(i):
    return hex(i).rstrip("L").lstrip("0x") or "0"

def int_to_string(integer, keyspace_chars):
    """ Turn a positive integer into a string. """
    if not integer > 0:
        raise ValueError('integer must be > 0')
    output = ""
    while integer > 0:
        integer, digit = divmod(integer, len(keyspace_chars))
        output += keyspace_chars[digit]
    return output[::-1]

def string_to_int(string, keyspace_chars):
    """ Turn a string into a positive integer. """
    output = 0
    for char in string:
        output = output * len(keyspace_chars) + keyspace_chars.index(char)
    return output

def change_keyspace(string, original_keyspace, target_keyspace):
    """ Convert a string from one keyspace to another. """
    assert isinstance(string, str)
    intermediate_integer = string_to_int(string, original_keyspace)
    output_string = int_to_string(intermediate_integer, target_keyspace)
    return output_string

def binary_sha256(s):
    return hashlib.sha256(s).digest()

def binary_hash160(s):
    return hashlib.new('ripemd160', binary_sha256(s)).digest()

def base58check_encode(s, version_byte=0):
    HEX_KEYSPACE = "0123456789abcdef"
    B58_KEYSPACE = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    s = chr(int(version_byte)) + s
    leading_bytes = len(re.match('^\x00*', s).group(0))
    checksum = binary_sha256(binary_sha256(s))[:4]
    hex_s = binascii.hexlify(s + checksum)
    
    return '1' * leading_bytes + change_keyspace(hex_s, HEX_KEYSPACE, B58_KEYSPACE)

def random_passphrase(phrase_length, word_list):
    random.seed(dev_random_entropy(64))
    passphrase_words = []
    for i in range(phrase_length):
        passphrase_words.append(random.choice(word_list))
    return " ".join(passphrase_words)

