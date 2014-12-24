# -*- coding: utf-8 -*-
"""
    coinrpc
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import json

from .config import NAMECOIND_SERVER


from .namecoind_client import NamecoindClient

from .config import NAMECOIND_SERVER, NAMECOIND_PORT, NAMECOIND_USER
from .config import NAMECOIND_PASSWD
from .config import MAIN_SERVER, LOAD_SERVERS

from multiprocessing.pool import ThreadPool
from commontools import log
from commontools import pretty_print as pprint


# -----------------------------------
def pending_transactions(server):

    """ get the no. of pending transactions (0 confirmations) on a server
    """

    namecoind = NamecoindClient(server, NAMECOIND_PORT,
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
            namecoind = NamecoindClient(server, NAMECOIND_PORT,
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


# -----------------------------------
def clean_wallet(server, clean_wallet):

    namecoind = NamecoindClient(server)

    reply = namecoind.listtransactions("", 10000)

    counter = 0
    counter_total = 0

    track_confirmations = 1000

    for i in reply:
        counter_total += 1

        if i['confirmations'] == 0:

            counter += 1

            if clean_wallet:
                log.debug(namecoind.deletetransaction(i['txid']))

        elif i['confirmations'] < track_confirmations:
            track_confirmations = i['confirmations']

    log.debug("%s: %s pending tx, %s confirmations (last tx), %s total tx"
              % (server, counter, track_confirmations, counter_total))


# -----------------------------------
def rebroadcast_tx(server, raw_tx):

    namecoind = NamecoindClient(server)

    print namecoind.sendrawtransaction(raw_tx)


# -----------------------------------
def check_servers(servers, clean=False):

    for server in servers:
        clean_wallet(server, clean)


# -----------------------------------
def get_confirmations(server, tx):

    namecoind = NamecoindClient(server)

    reply = namecoind.listtransactions("",10000)

    for entry in reply:

        if entry['txid'] == tx:
            return int(entry['confirmations'])

    return 0

# -----------------------------------
if __name__ == '__main__':

    try:
        option = sys.argv[1]
        if(option == '--clean'):
            check_servers(LOAD_SERVERS, clean=True)
        exit(0)
    except:
        pass

    check_servers(LOAD_SERVERS, clean=False)
    