# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os, binascii
from utilitybelt import dev_random_entropy, dev_urandom_entropy

def random_secret_exponent(curve_order):
    """ Generates a random secret exponent. """
    # run a rejection sampling algorithm to ensure the random int is less
    # than the curve order
    while True:
        # generate a random 256 bit hex string
        random_hex = binascii.hexlify(dev_random_entropy(32))
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            break
    return random_int
