# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
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

def fit_num_in_range(num, lower_bound, upper_bound):
    """ Fits the number so that it is greater than or equal to the lower bound
        and less than the upper bound.
    """
    assert(isinstance(upper_bound, (int, long))
        and isinstance(lower_bound, (int, long)) and upper_bound > lower_bound)
    value_range = upper_bound - lower_bound
    offset = num % value_range
    return offset + lower_bound

def random_secret_exponent(curve_order):
    """ Generates a random secret exponent. """
    random_256bit_hex_string = binascii.hexlify(get_entropy(32))
    random_256bit_int = int(random_256bit_hex_string, 16)
    int_secret_exponent = fit_num_in_range(random_256bit_int, 1, curve_order)
    return int_secret_exponent
