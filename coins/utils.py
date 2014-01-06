# -*- coding: utf-8 -*-
"""
    Coins
    ~~~~~
    
    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import re
import random
import hashlib
import binascii

def fit_number_in_range(num, lower_bound, upper_bound):
    assert(isinstance(upper_bound, (int, long))
        and isinstance(lower_bound, (int, long)) and upper_bound > lower_bound)
    while num > upper_bound:
        num -= (upper_bound - lower_bound)
    while num < lower_bound:
        num += (upper_bound - lower_bound)
    return num

""" base/keyspace conversion """

HEX_KEYSPACE = "0123456789abcdef"
B58_KEYSPACE = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

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

""" random number / passphrase operations """

def dev_random_entropy(numbytes):
    return open("/dev/random", "rb").read(numbytes)

def dev_urandom_entropy(numbytes):
    return open("/dev/urandom", "rb").read(numbytes)

def get_entropy(numbytes):
    if os.name == 'nt':
        return os.urandom(numbytes)
    else:
        return dev_random_entropy(numbytes)

def random_secret_exponent(curve_order):
    """ Generates a random secret exponent. """
    random_256bit_hex_string = binascii.hexlify(get_entropy(32))
    random_256bit_int = int(random_256bit_hex_string, 16)
    int_secret_exponent = fit_number_in_range(random_256bit_int, 1, curve_order)

    return int_secret_exponent

from .words import TOP_65536_ENGLISH_WORDS
from math import pow, ceil, log

def random_passphrase_from_wordlist(phrase_length, wordlist):
    """ An extremely entropy efficient passphrase generator.

        This function:
        -Pulls entropy from the safer alternative to /dev/urandom: /dev/random
        -Doesn't rely on random.seed (words are selected right from the entropy)
        -Only requires 2 entropy bytes/word for word lists of up to 65536 words
    """

    passphrase_words = []
    
    numbytes_of_entropy = phrase_length * 2
    entropy = list(get_entropy(numbytes_of_entropy))

    bytes_per_word = int(ceil(log(len(wordlist), 2) / 8))

    if (phrase_length * bytes_per_word > 64):
        raise Exception("Error! This operation requires too much entropy. \
            Try a shorter phrase length or word list.")

    for i in range(phrase_length):
        current_entropy = entropy[i*bytes_per_word:(i+1)*bytes_per_word]
        index = int(''.join(current_entropy).encode('hex'), 16) % len(wordlist)
        word = wordlist[index]
        passphrase_words.append(word)

    return " ".join(passphrase_words)

def random_160bit_passphrase():
    word_list = TOP_65536_ENGLISH_WORDS
    return random_passphrase_from_wordlist(12, word_list[0:10500])

def random_256bit_passphrase():
    word_list = TOP_65536_ENGLISH_WORDS
    return random_passphrase_from_wordlist(16, word_list[0:65536])

""" sha256 operations """

def binary_sha256(s):
    return hashlib.sha256(s).digest()

def binary_hash160(s):
    return hashlib.new('ripemd160', binary_sha256(s)).digest()

def binary_checksum(s):
    """ Takes in a binary string and returns a checksum. """
    return binary_sha256(binary_sha256(s))[:4]

""" base 58 check operations """

def b58check_encode(bin_s, version_byte=0):
    """ Takes in a binary string and converts it to a base 58 check string. """
    # append the version byte to the beginning
    bin_s = chr(int(version_byte)) + bin_s
    # calculate the number of leading zeros
    num_leading_zeros = len(re.match('^\x00*', bin_s).group(0))
    # add in the checksum add the end
    bin_s = bin_s + binary_checksum(bin_s)
    # convert from b2 to b16
    hex_s = binascii.hexlify(bin_s)
    # convert from b16 to b58
    b58_s = change_keyspace(hex_s, HEX_KEYSPACE, B58_KEYSPACE)

    return B58_KEYSPACE[0] * num_leading_zeros + b58_s

def b58check_unpack(b58check_s):
    """ Takes in a base 58 check string and returns: the version byte, the
        original encoded binary string, and the checksum.
    """
    # convert from b58 to b16
    hex_s = change_keyspace(b58check_s, B58_KEYSPACE, HEX_KEYSPACE)
    # convert from b16 to b2
    bin_s = binascii.unhexlify(hex_s)
    # make sure the newly calculated checksum equals the embedded checksum
    assert binary_checksum(bin_s[:-4]) == bin_s[-4:]
    # add in the leading zeros
    num_leading_zeros = len(re.match('^1*', b58check_s).group(0))
    padded_bin_s = '\x00' * num_leading_zeros + bin_s
    # return values
    version_byte = padded_bin_s[:1]
    encoded_value = padded_bin_s[1:-4]
    checksum = padded_bin_s[-4:]
    return version_byte, encoded_value, checksum

def b58check_decode(b58check_s):
    """ Takes in a base 58 check string and returns the original encoded binary
        string.
    """
    version_byte, encoded_value, checksum = b58check_unpack(b58check_s)
    return encoded_value

def b58check_version_byte(b58check_s):
    """ Takes in a base 58 check string and returns the version byte as an
        integer. """
    version_byte, encoded_value, checksum = b58check_unpack(b58check_s)
    return ord(version_byte)

""" Format checking """

import ecdsa

def is_hex(s):
    try:
        int(s, 16)
    except ValueError:
        return False
    else:
        return True

def is_valid_b58check(b58check_s):
    version_byte, binary_s, checksum = b58check_unpack(b58check_s)
    if b58check_s == b58check_encode(binary_s, version_byte=ord(version_byte)):
        return True
    else:
        return False

def is_valid_secret_exponent(val, curve_order):
    return (isinstance(val, (int, long)) and val >= 1 and val < curve_order)

def is_256bit_hex_string(val):
    return (isinstance(val, str) and len(val) == 64 and is_hex(val))

def is_wallet_import_format(val):
    return (len(val) == 51 and is_valid_b58check(val))

def is_valid_b58check_address(s):
    return (len(s) == 34 and is_valid_b58check(s))

def extract_pk_as_int(pk, curve_order):
    if isinstance(pk, int):
        secret_exponent = pk
    elif is_256bit_hex_string(pk):
        secret_exponent = int(pk, 16)
    elif is_wallet_import_format(pk):
        secret_exponent = int(binascii.hexlify(b58check_decode(pk)), 16)
    else:
        raise ValueError("Private key is not in a valid format (int, wif, or hex).")

    # make sure that: 1 <= secret_exponent < curve_order
    if is_valid_secret_exponent(secret_exponent, curve_order):
        return secret_exponent
    else:
        raise IndexError("Secret exponent is outside of the valid range. Must be >= 1 and < the curve order.")

