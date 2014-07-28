#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

"""
	three use cases of coinrpc:
	a) use HTTP API for namecoind cluster (read-only)
	b) get access to a namecoind server (read/write)
	c) get access to a bitcoind server (read/write)
"""

from .flask_api import app
from .namecoin import namecoind
from .bitcoin import bitcoind

from .config import *