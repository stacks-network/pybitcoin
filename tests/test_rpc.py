#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Hack around absolute paths
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")

sys.path.insert(0, parent_dir)

import unittest
from pybitcoin.rpc import BitcoindClient, NamecoindClient

bitcoind = BitcoindClient()
namecoind = NamecoindClient()


class NamecoindTestCase(unittest.TestCase):

    def test_connectivity(self):
        """ Check if can connect to namecoind
        """

        blocks = namecoind.blocks()
        self.assertIsNotNone(blocks, msg='Namecoind is not responding')

    def test_full_profile(self):
        """ Check if can connect to namecoind
        """

        key = 'u/muneeb'

        profile = namecoind.get_full_profile(key)
        self.assertIsInstance(profile, dict, msg='Could not get full profile')


class BitcoindTestCase(unittest.TestCase):

    def test_connectivity(self):
        """ Check if can connect to bitcoind
        """

        blocks = bitcoind.blocks()
        self.assertIsNotNone(blocks, msg='Bitcoind is not responding')

if __name__ == '__main__':

    unittest.main()
