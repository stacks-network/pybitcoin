# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

# data structure constants
UINT_MAX = 2**32-1

# protocol constants
SATOSHIS_PER_COIN = 10**8
MAX_BYTES_AFTER_OP_RETURN = 80

# fee defaults
STANDARD_FEE = 1000  # 1000 satoshis = 10 bits = .01 mbits = .00001 BTC
OP_RETURN_FEE = 10000  # 10k satoshis = .0001 BTC
