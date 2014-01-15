# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2013 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import binascii

def dev_random_entropy(numbytes):
    return open("/dev/random", "rb").read(numbytes)

def dev_urandom_entropy(numbytes):
    return open("/dev/urandom", "rb").read(numbytes)

def get_entropy(numbytes):
    if os.name == 'nt':
        return os.urandom(numbytes)
    else:
        return dev_random_entropy(numbytes)

def fit_number_in_range(num, lower_bound, upper_bound):
    assert(isinstance(upper_bound, (int, long))
        and isinstance(lower_bound, (int, long)) and upper_bound > lower_bound)
    while num > upper_bound:
        num -= (upper_bound - lower_bound)
    while num < lower_bound:
        num += (upper_bound - lower_bound)
    return num

def random_secret_exponent(curve_order):
    """ Generates a random secret exponent. """
    random_256bit_hex_string = binascii.hexlify(get_entropy(32))
    random_256bit_int = int(random_256bit_hex_string, 16)
    int_secret_exponent = fit_number_in_range(random_256bit_int, 1, curve_order)

    return int_secret_exponent
