#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import json

from coinrpc.namecoind_server import NamecoindClient

from config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER
from config import NAMECOIND_PASSWD
from config_local import MAIN_SERVER, LOAD_SERVERS

from multiprocessing.pool import ThreadPool
from commontools import log


# -----------------------------------
def pending_transactions(server):

    """ get the no. of pending transactions (0 confirmations) on a server
    """

    namecoind = NamecoindServer(server, NAMECOIND_PORT,
                                NAMECOIND_USER, NAMECOIND_PASSWD)

    reply = namecoind.listtransactions("", 10000)

    counter = 0

    for i in reply:
        if i['confirmations'] == 0:
            counter += 1

    return counter


# -----------------------------------
def check_address(address):

    reply = {}
    reply["server"] = None
    reply["ismine"] = False
    reply['registered'] = True

    # --------------------------
    def check_address_inner(server):

        try:
            namecoind = NamecoindServer(server, NAMECOIND_PORT,
                                        NAMECOIND_USER, NAMECOIND_PASSWD)

            info = namecoind.validate_address(address)
        except Exception as e:
            log.debug("Error in server %s", server)
            log.debug(e)
            return

        if info['ismine'] is True:
            reply['server'] = server
            reply['ismine'] = True

    # first check the main server
    check_address_inner(MAIN_SERVER)

    if reply['ismine'] is True:
        return reply

    # if not main server, check others
    pool = ThreadPool(len(LOAD_SERVERS))

    pool.map(check_address_inner, LOAD_SERVERS)
    pool.close()
    pool.join()

    return reply


# -----------------------------------
def get_server(key):

    """ given a key, get the IP address of the server that has the pvt key that
        owns the name/key
    """

    namecoind = NamecoindClient(NAMECOIND_SERVER, NAMECOIND_PORT,
                                NAMECOIND_USER, NAMECOIND_PASSWD)

    info = namecoind.name_show(key)

    if 'address' in info:
        return check_address(info['address'])

    response = {}
    response["registered"] = False
    response["server"] = None
    response["ismine"] = False
    return response
