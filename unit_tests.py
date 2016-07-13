# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json
import traceback
import unittest
from test import test_support

from pybitcoin.publickey import BitcoinPublicKey
from pybitcoin.privatekey import BitcoinPrivateKey, NamecoinPrivateKey
from pybitcoin.keypair import BitcoinKeypair
from pybitcoin.rpc import BitcoindClient
from pybitcoin.wallet import SDWallet
from pybitcoin.merkle import MerkleTree, calculate_merkle_root

from pybitcoin.b58check import b58check_encode, b58check_decode, b58check_unpack
from pybitcoin.formatcheck import is_b58check_address, is_256bit_hex_string, \
    is_wif_pk

from pybitcoin.transactions import analyze_private_key
from pybitcoin.transactions.network import make_send_to_address_tx, \
    make_op_return_tx, send_to_address, broadcast_transaction

from pybitcoin.services import blockcypher
from pybitcoin.services import blockchain_info
from pybitcoin.services.bitcoind import create_bitcoind_service_proxy

from pybitcoin import PrivateKeychain, PublicKeychain

get_class = lambda x: globals()[x]

from settings import BITCOIND_RPC_PASSWORD, BITCOIND_RPC_USERNAME, \
    BLOCKCHAIN_API_KEY, BLOCKCYPHER_API_KEY, \
    BITCOIN_PRIVATE_KEY, BITCOIN_PRIVATE_KEY_2

bitcoind_client = BitcoindClient(
    server='btcd.onename.com', port=8332, user=BITCOIND_RPC_USERNAME,
    passwd=BITCOIND_RPC_PASSWORD, use_https=True)


_reference_info = {
    'passphrase': 'correct horse battery staple',
    'bin_private_key': '\xc4\xbb\xcb\x1f\xbe\xc9\x9de\xbfY\xd8\\\x8c\xb6.\xe2\xdb\x96?\x0f\xe1\x06\xf4\x83\xd9\xaf\xa7;\xd4\xe3\x9a\x8a',
    'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
    'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
    'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
    'wif_private_key': '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
    'address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
    'wif_version_byte': 128,
    'pem_private_key': '-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIMS7yx++yZ1lv1nYXIy2LuLblj8P4Qb0g9mvpzvU45qKoAcGBSuBBAAK\noUQDQgAEeNQwJ0+MXsEyEzgVHp8n9MZ2oAi9+GONB8C2vpqzXHGhUYBjJDrNTf6W\ntm4/LsgBPI4HLNCbODShn4H2Wcw0VQ==\n-----END EC PRIVATE KEY-----\n',
    'pem_public_key': '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEeNQwJ0+MXsEyEzgVHp8n9MZ2oAi9+GON\nB8C2vpqzXHGhUYBjJDrNTf6Wtm4/LsgBPI4HLNCbODShn4H2Wcw0VQ==\n-----END PUBLIC KEY-----\n',
    'der_private_key': '30740201010420c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8aa00706052b8104000aa1440342000478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
    'der_public_key': '3056301006072a8648ce3d020106052b8104000a0342000478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455'
}


class BitcoinUncompressedPublicKeyTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        self.public_key = BitcoinPublicKey(self.reference['hex_public_key'])

    def tearDown(self):
        pass

    def test_address(self):
        self.assertEqual(self.public_key.address(), self.reference['address'])

    def test_hex_hash160(self):
        self.assertEqual(
            self.public_key.hash160(), self.reference['hex_hash160'])

    def test_hex_public_key(self):
        self.assertEqual(
            self.public_key.to_hex(), self.reference['hex_public_key'])

    def test_pem_public_key(self):
        self.assertEqual(
            self.public_key.to_pem(), self.reference['pem_public_key'])

    def test_der_public_key(self):
        self.assertEqual(
            self.public_key.to_der(), self.reference['der_public_key'])


class BitcoinCompressedPublicKeyTest(unittest.TestCase):
    def setUp(self):
        self.reference = {
            'hex_public_key': '02068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7',
            'bin_public_key': '\x02\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7',
            'hex_hash160': '25488b0d3bb770d6e0ef07e1f19d33ab59931dee',
            'bin_hash160': '%H\x8b\r;\xb7p\xd6\xe0\xef\x07\xe1\xf1\x9d3\xabY\x93\x1d\xee',
            'address': '14Q8uVAX29RUMvqPGXL5sg6NiwwMRFCm8C',
        }
        self.public_key = BitcoinPublicKey(self.reference['hex_public_key'])

    def tearDown(self):
        pass

    def test_address(self):
        self.assertEqual(self.public_key.address(), self.reference['address'])

    def test_bin_hash160(self):
        self.assertEqual(
            self.public_key.bin_hash160(), self.reference['bin_hash160'])

    def test_hex_hash160(self):
        self.assertEqual(
            self.public_key.hash160(), self.reference['hex_hash160'])

    def test_bin_public_key(self):
        self.assertEqual(
            self.public_key.to_bin(), self.reference['bin_public_key'])

    def test_hex_public_key(self):
        self.assertEqual(
            self.public_key.to_hex(), self.reference['hex_public_key'])


class BitcoinPublicKeyCreationTest(unittest.TestCase):
    def setUp(self):
        self.address_compressed = '14Q8uVAX29RUMvqPGXL5sg6NiwwMRFCm8C'
        self.address_uncompressed = '1AuZor1RVzG22wqbH2sG2j5WRDZsbw1tip'

    def tearDown(self):
        pass

    def test_create_pubkey_from_hex_uncompressed_format(self):
        public_key_string = '04068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7b2832f87f683100b89c2e95314deeeacbc6409af1e36c3ae3fd8c5f2f243cfec'
        self.assertEqual(self.address_uncompressed, BitcoinPublicKey(
            public_key_string).address())

    def test_create_pubkey_from_bin_uncompressed_format(self):
        public_key_string = '\x04\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7\xb2\x83/\x87\xf6\x83\x10\x0b\x89\xc2\xe9S\x14\xde\xee\xac\xbcd\t\xaf\x1e6\xc3\xae?\xd8\xc5\xf2\xf2C\xcf\xec'
        self.assertEqual(self.address_uncompressed, BitcoinPublicKey(
            public_key_string).address())

    def test_create_pubkey_from_hex_ecdsa_format(self):
        public_key_string = '068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7b2832f87f683100b89c2e95314deeeacbc6409af1e36c3ae3fd8c5f2f243cfec'
        self.assertEqual(self.address_uncompressed, BitcoinPublicKey(
            public_key_string).address())

    def test_create_pubkey_from_bin_ecdsa_format(self):
        public_key_string = '\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7\xb2\x83/\x87\xf6\x83\x10\x0b\x89\xc2\xe9S\x14\xde\xee\xac\xbcd\t\xaf\x1e6\xc3\xae?\xd8\xc5\xf2\xf2C\xcf\xec'
        self.assertEqual(self.address_uncompressed, BitcoinPublicKey(
            public_key_string).address())

    def test_create_pubkey_from_hex_compressed_format(self):
        public_key_string = '02068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7'
        self.assertEqual(self.address_compressed, BitcoinPublicKey(
            public_key_string).address())

    def test_create_pubkey_from_bin_compressed_format(self):
        public_key_string = '\x02\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7'
        self.assertEqual(self.address_compressed, BitcoinPublicKey(
            public_key_string).address())


class BitcoinPrivateKeyToPublicKeyTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_private_key_to_public_key_conversion(self):
        priv = BitcoinPrivateKey(self.reference['hex_private_key'])
        pub = priv.public_key()
        self.assertEqual(pub.to_hex(), self.reference['hex_public_key'])
        self.assertEqual(pub.address(), self.reference['address'])


class BitcoinPrivateKeyTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        self.private_key = BitcoinPrivateKey(self.reference['hex_private_key'])

    def tearDown(self):
        pass

    def test_private_key_from_wif(self):
        self.private_key_from_wif = BitcoinPrivateKey(
            self.reference['wif_private_key'])
        self.assertEqual(
            self.private_key.to_hex(), self.private_key_from_wif.to_hex())

    def test_hex_private_key(self):
        self.assertEqual(
            self.private_key.to_hex(), self.reference['hex_private_key'])

    def test_wif_private_key(self):
        self.assertEqual(
            self.private_key.to_wif(), self.reference['wif_private_key'])

    def test_pem_private_key(self):
        self.assertEqual(
            self.private_key.to_pem(), self.reference['pem_private_key'])

    def test_der_private_key(self):
        self.assertEqual(
            self.private_key.to_der(), self.reference['der_private_key'])


class BitcoinKeypairTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        self.keypair = BitcoinKeypair(self.reference['hex_private_key'])

    def tearDown(self):
        pass

    def test_hex_private_key(self):
        self.assertEqual(
            self.keypair.private_key(), self.reference['hex_private_key'])

    def test_wif_private_key(self):
        self.assertEqual(
            self.keypair.wif_pk(), self.reference['wif_private_key'])

    def test_address(self):
        self.assertEqual(
            self.keypair.address(), self.reference['address'])

    def test_hex_hash160(self):
        self.assertEqual(self.keypair.hash160(), self.reference['hex_hash160'])

    def test_public_key(self):
        self.assertEqual(
            self.keypair.public_key(), self.reference['hex_public_key'])


class AltcoinKeypairTest(unittest.TestCase):
    coin_names = [
        'bitcoin', 'litecoin', 'namecoin', 'peercoin', 'primecoin',
        'dogecoin', 'worldcoin', 'feathercoin', 'terracoin', 'novacoin',
        'testnet', 'protoshares', 'memorycoin', 'quarkcoin', 'infinitecoin',
        'cryptogenicbullion', 'ixcoin', 'anoncoin', 'megacoin'
    ]

    reference = {
        'passphrase': 'correct horse battery staple',
        'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
        'hex_public_key': '78d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
        'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
        ('bitcoin', 'wif'): '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
        ('bitcoin', 'address'): '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
        ('litecoin', 'wif'): '6vcfLvDpYnHdbVxoQa6Lmo3k9iR5xVjKwwf3dp4XgmQT3QJywYi',
        ('litecoin', 'address'): 'LdAPi7uXrLLmeh7u57pzkZc3KovxEDYRJq',
        ('namecoin', 'wif'): '74Pe3r1wxUzY8nHd2taLb5SqpAsxZK6q6VwUcQp7fPS11tYZd9P',
        ('namecoin', 'address'): 'NEWoeZ6gh4CGvRgFAoAGh4hBqpxizGT6gZ',
        ('peercoin', 'wif'): '7ADsaYN3Wm2DYF2jkdSLT3FAZWj7WRdTTR9oLrsoeMTAVgq1Mho',
        ('peercoin', 'address'): 'PSXcbszYpbauNj6WF4AE9SWYjLjZArBajH',
        ('primecoin', 'wif'): '6623w812F9NyDzSAk5aMvn4PFs28htfSGxtMY4s7qPEkhoV8sQS',
        ('primecoin', 'address'): 'AZiK6QTL6pksCrdjTdW2dRoNbCVNQ7zRs6',
        ('dogecoin', 'wif'): '6KdGAk9FD87ZAjW768vMc2FoffLAFpZZnSP7F7gPnyHUA9ttj7B',
        ('dogecoin', 'address'): 'DP5XzAYM55zzvtcLdZqG2JhszjHyNnvW8i',
        ('worldcoin', 'wif'): '7mDGkiScrRCHy1VS54cKcp373Zp3D6oDcvRjjZFwY9a9NushHNZ',
        ('worldcoin', 'address'): 'WgcUKqMjbqvg6Xc4gc9xshQi4RNY1S38TD',
        ('feathercoin', 'wif'): '5nXMM2xjaKHw1cCparzNLtfR1qUfrZ5ZCDFPLig3tVBGGBK2QwG',
        ('feathercoin', 'address'): '6wftERmjiCayqxNxErWAGJMHvfAt4RZZbn',
        ('terracoin', 'wif'): '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
        ('terracoin', 'address'): '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
        ('novacoin', 'wif'): '5artHeGYTmEaCgib9PGNcy4mX9nMxL2JUNpjspYfvZ8wJWQjuBJ',
        ('novacoin', 'address'): '4XeGKmz1T7oiwMYS6LWFMYia9ddDoT6ajT',
        ('ixcoin', 'wif'): 'Mw64RiX6A23DKVivM4USZXC8nBt3bqyKquB8wsifzJ589JYYDF',
        ('ixcoin', 'address'): 'xqagKtjTka3dFhfhGsogPr6qyD7rAzGQKQ',
        ('testnet', 'wif'): '935ZTXVqEatu6BaEX6CHrzpXquDKurpVXD7q1FQ1K3pt8VwmG2L',
        ('testnet', 'address'): 'myTPjxggahXyAzuMcYp5JTkbybANyLsYBW',
        ('protoshares', 'wif'): '7CAckmp5NBhSg4cSfD4LQMqwUdLqA8ULF4Dub1Zhe1TYzJcerWL',
        ('protoshares', 'address'): 'PqsDazHqXn3nCAEbGUVYdZnLMqzVqdmE9z',
        ('memorycoin', 'wif'): '6zW9hP7tFde5s98DDjLLgSFHyweXFuR5XDoG87SKg5RE2dHMpaF',
        ('memorycoin', 'address'): 'MRqbgLW7GhGXHZQ57xVdip9capSqZatiut',
        ('quarkcoin', 'wif'): '7G477Ei9533twhmrUNJLK13VJraGTYA5pLN85JwVdKUKyd6oDz6',
        ('quarkcoin', 'address'): 'QeYRZCtQx8yXq2WmKKABbpKucrWPFn2Z8g',
        ('infinitecoin', 'wif'): '8jarsSTYZkorsoLtMscJH7RZbsfs4XEcSTUrouCwN9mPgw1j4iq',
        ('infinitecoin', 'address'): 'iMQxsz16C5N5p6eaPmpCwLJXK3qtXZuvoh',
        ('cryptogenicbullion', 'wif'): '5gh7pLce23GFc9Ths88NUvs6GVdWuSYvqJ34cGcMuXA6nPooqdc',
        ('cryptogenicbullion', 'address'): '5jf5H6ssafCMPexhAbWCovXw39Q3ryw5ic',
        ('anoncoin', 'wif'): '6623w812F9NyDzSAk5aMvn4PFs28htfSGxtMY4s7qPEkhoV8sQS',
        ('anoncoin', 'address'): 'AZiK6QTL6pksCrdjTdW2dRoNbCVNQ7zRs6',
        ('megacoin', 'wif'): '6zW9hP7tFde5s98DDjLLgSFHyweXFuR5XDoG87SKg5RE2dHMpaF',
        ('megacoin', 'address'): 'MRqbgLW7GhGXHZQ57xVdip9capSqZatiut',
    }

    def setUp(self):
        pass

    def tearDown(self):
        pass


class BitcoinBrainWalletKeypairTest(BitcoinKeypairTest):
    def setUp(self):
        BitcoinKeypairTest.setUp(self)
        self.keypair = BitcoinKeypair.from_passphrase(
            self.reference['passphrase'])

    def test_passphrase(self):
        self.assertEqual(
            self.keypair.passphrase(), self.reference['passphrase'])

    def test_random_passphrase_length(self):
        random_keypair = BitcoinKeypair.from_passphrase()
        self.assertTrue(len(random_keypair.passphrase().split()) > 1)


class BitcoinKeypairFromWIFTest(BitcoinKeypairTest):
    def setUp(self):
        BitcoinKeypairTest.setUp(self)
        self.keypair = BitcoinKeypair.from_private_key(
            self.reference['wif_private_key'])


class RandomBitcoinKeypairsTest(unittest.TestCase):
    def setUp(self):
        self.keypair = BitcoinKeypair()
        self.brainwallet_keypair = BitcoinKeypair.from_passphrase()

    def tearDown(self):
        pass

    def test_keypair(self):
        # self.assertTrue(is_256bit_hex_string(self.keypair.private_key()))
        # self.assertTrue(is_wif_pk(self.keypair.wif_pk()))
        self.assertTrue(is_b58check_address(self.keypair.address()))

    def test_brainwallet_keypair(self):
        self.assertTrue(len(self.brainwallet_keypair.passphrase().split()) > 1)


class BitcoinB58CheckTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_b58check_encode_then_decode(self):
        bin_private_key = self.reference['hex_private_key'].decode('hex')
        wif_private_key = b58check_encode(
            bin_private_key, version_byte=self.reference['wif_version_byte'])
        self.assertEqual(self.reference['wif_private_key'], wif_private_key)
        bin_private_key_verification = b58check_decode(wif_private_key)
        self.assertEqual(bin_private_key_verification, bin_private_key)

    def test_b58check_unpack_then_encode(self):
        version_byte, bin_private_key, checksum = b58check_unpack(
            self.reference['wif_private_key'])
        self.assertTrue(
            ord(version_byte) == self.reference['wif_version_byte'])
        wif_private_key = b58check_encode(
            bin_private_key, version_byte=ord(version_byte))
        self.assertEqual(self.reference['wif_private_key'], wif_private_key)


class BitcoinFormatCheckTest(unittest.TestCase):
    reference = _reference_info

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_wif_private_key(self):
        self.assertTrue(is_wif_pk(self.reference['wif_private_key']))

    def test_is_hex_private_key(self):
        self.assertTrue(
            is_256bit_hex_string(self.reference['hex_private_key']))


class SequentialWalletTest(unittest.TestCase):
    reference = {
        'passphrase': ('shepherd mais pack rate enamel horace diva filesize'
                       ' maximum really roar mall'),
        'bitcoin_keypair_1': {
            'address': '1DS2vmsqTwtXp1DfmDHi55Aqc6w4LBUC9k',
        }
    }

    def setUp(self):
        self.wallet = SDWallet(self.reference['passphrase'])

    def tearDown(self):
        pass

    def test_bitcoin_keypairs(self):
        bitcoin_keypair_1 = self.wallet.keypair(1, BitcoinKeypair)
        self.assertEqual(self.reference['bitcoin_keypair_1']['address'],
                         bitcoin_keypair_1.address())
        self.assertEqual(bitcoin_keypair_1.passphrase(),
                         self.reference['passphrase'] + ' bitcoin1')

UNSPENTS_DICT = {
    '691d1645dc6f9431fe2ef414aaa88887efb5fed9354bf53ed01349595bf725ed': {
        'script_hex': '76a9148eac3d867e1f92f47da40217c3cbd3d75d05701388ac',
        'output_index': 1,
        'transaction_hash': ("691d1645dc6f9431fe2ef414aaa88887efb5fed9354bf"
                             "53ed01349595bf725ed"),
        'confirmations': 6146,
        'value': 55366270
    }
}


class ServicesGetUnspentsTest(unittest.TestCase):
    def setUp(self):
        self.address = '1E1PHi525xnHvSU4BqnV8aqwZwN8zoaHFv'
        self.total_unspent_value = 55366270
        self.unspents_dict = UNSPENTS_DICT

    def tearDown(self):
        pass

    def compare_unspents(self, unspents):
        for unspent in unspents:
            if unspent['transaction_hash'] in self.unspents_dict:
                ref_unspent = self.unspents_dict[unspent['transaction_hash']]
                self.assertEqual(
                    unspent['transaction_hash'],
                    ref_unspent['transaction_hash'])
                self.assertEqual(
                    unspent['output_index'], ref_unspent['output_index'])
                self.assertEqual(
                    unspent['script_hex'], ref_unspent['script_hex'])
                self.assertEqual(unspent['value'], ref_unspent['value'])
            else:
                continue

    def compare_total_value(self, unspents):
        total_value = sum([u['value'] for u in unspents])
        self.assertEqual(total_value, self.total_unspent_value)

    def test_blockcypher_get_unspents(self):
        client = blockcypher.BlockcypherClient()
        unspents = blockcypher.get_unspents(self.address, client)
        self.compare_total_value(unspents)
        self.compare_unspents(unspents)

    """
    def test_blockchain_info_get_unspents(self):
        client = blockchain_info.BlockchainInfoClient(
            BLOCKCHAIN_API_KEY)
        unspents = blockchain_info.get_unspents(self.address, client)
        self.compare_total_value(unspents)
        self.compare_unspents(unspents)
    """

    """
    def test_bitcoind_get_unspents(self):
        client = bitcoind_client
        unspents = client.get_unspents(self.address)
        self.compare_total_value(unspents)
        self.compare_unspents(unspents)
    """


class TransactionNetworkFunctionsTest(unittest.TestCase):
    def setUp(self):
        self.private_key = BITCOIN_PRIVATE_KEY

    def tearDown(self):
        pass

    def test_analyze_private_key(self):
        client = blockcypher.BlockcypherClient(BLOCKCYPHER_API_KEY)
        private_key_obj, from_address, inputs = analyze_private_key(
            self.private_key, client)
        self.assertTrue(isinstance(private_key_obj, BitcoinPrivateKey))


class ServicesSendTransactionTest(unittest.TestCase):
    def setUp(self):
        self.recipient_address = '1EEwLZVZMc2EhMf3LXDARbp4mA3qAwhBxu'
        self.private_key = BitcoinPrivateKey(BITCOIN_PRIVATE_KEY)
        self.send_amount = 1000

        self.blockcypher_client = blockcypher.BlockcypherClient(
            BLOCKCYPHER_API_KEY)
        self.blockchain_info_client = blockchain_info.BlockchainInfoClient(
            BLOCKCHAIN_API_KEY)
        self.bitcoind_client = bitcoind_client
        self.bitcoind = create_bitcoind_service_proxy(
            BITCOIND_RPC_USERNAME, BITCOIND_RPC_PASSWORD)

        self.signed_tx = make_send_to_address_tx(
            self.recipient_address, self.send_amount,
            self.private_key, self.blockcypher_client)

    def tearDown(self):
        pass

    def broadcast_with_client(self, tx, client):
        return broadcast_transaction(tx, client)

    def send_to_address_with_client(self, client):
        return send_to_address(
            self.recipient_address, 1000, self.private_key, client)

    """
    def test_send_transaction_blockcypher_com(self):
        resp = self.broadcast_with_client(
            self.signed_tx, self.blockcypher_client)
        self.assertTrue(resp.get('success'))

    def test_send_transaction_blockchain_info(self):
        resp = self.broadcast_with_client(
            self.signed_tx, self.blockchain_info_client)
        self.assertTrue(resp.get('success'))

    def test_send_transaction_bitcoind(self):
        resp = self.broadcast_with_client(self.signed_tx, self.bitcoind)
        self.assertTrue(resp.get('success'))
    """

    """
    def test_build_transaction(self):
        signed_tx = make_send_to_address_tx(
            recipient_address, 1000, private_key, client)
        #print signed_tx
        self.assertTrue(True)
    """


class ServicesSendOpReturnTransactionTest(unittest.TestCase):
    def setUp(self):
        self.private_key = BITCOIN_PRIVATE_KEY_2

        self.blockcypher_client = blockcypher.BlockcypherClient(
            BLOCKCYPHER_API_KEY)
        self.blockchain_info_client = blockchain_info.BlockchainInfoClient(
            BLOCKCHAIN_API_KEY)
        self.bitcoind_client = bitcoind_client

        self.fee = 10000

    def tearDown(self):
        pass

    def run_op_return_tx_building(self, data, client, format='bin'):
        return make_op_return_tx(
            data, self.private_key, client, fee=self.fee, format=format)

    def run_tx_broadcasting(self, tx, client):
        return broadcast_transaction(tx, client)

    """
    def run_data_embedding(self, data, client):
        resp = embed_data_in_blockchain(data, self.private_key,
            client, format='hex', fee=100000)
        return resp
    """

    def test_hex_op_return_tx(self):
        data = '00' * 80
        signed_tx = self.run_op_return_tx_building(
            data, self.blockcypher_client, format='hex')
        resp = self.run_tx_broadcasting(signed_tx, self.blockcypher_client)
        self.assertTrue(resp.get('success'))

    """
    def test_short_hex_op_return_tx(self):
        resp = embed_data('0'*2)
        self.assertTrue(resp.get('success'))
    
    def test_bin_op_return_tx(self):
        resp = embed_data("Hello, Blockchain!")
        self.assertTrue(resp.get('success'))
    """


class MerkleTest(unittest.TestCase):
    def setUp(self):
        self.hashes = [
            'f484b014c55a43b409a59de3177d49a88149b4473f9a7b81ea9e3535d4b7a301',
            '7b5636e9bc6ec910157e88702699bc7892675e8b489632c9166764341a4d4cfe',
            'f8b02b8bf25cb6008e38eb5453a22c502f37e76375a86a0f0cfaa3c301aa1209'
        ]
        self.merkle_root = ("4f4c8c201e85a64a410cc7272c77f443d8b8df3289c67af"
                            "9dab1e87d9e61985e")

    def tearDown(self):
        pass

    def test_merkle_tree(self):
        merkle_tree = MerkleTree(self.hashes)
        self.assertEqual(merkle_tree.root(), self.merkle_root)

    def test_calculate_merkle_root(self):
        merkle_root = calculate_merkle_root(self.hashes)
        self.assertEqual(merkle_root, self.merkle_root)


class KeychainTest(unittest.TestCase):
    def setUp(self):
        self.private_keychains = {
            "root": "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi",
            "0H": "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7",
            "0H/1": "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs",
            "0H/1/2H": "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM",
            "0H/1/2H/2": "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334",
            "0H/1/2H/2/1000000000": "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"
        }
        self.public_keychains = {
            "root": "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8",
            "0H": "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw",
            "0H/1": "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ",
            "0H/1/2H": "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5",
            "0H/1/2H/2": "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV",
            "0H/1/2H/2/1000000000": "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        }
        self.root_private_keychain = PrivateKeychain(self.private_keychains["root"])

    def tearDown(self):
        pass

    def test_root_private_to_public(self):
        public_keychain = self.root_private_keychain.public_keychain()
        self.assertEqual(str(public_keychain), str(self.public_keychains["root"]))

    def test_hardened_child_0H(self):
        private_keychain = self.root_private_keychain.hardened_child(0)
        self.assertEqual(str(private_keychain), str(self.private_keychains["0H"]))
        self.assertEqual(str(private_keychain.public_keychain()), str(self.public_keychains["0H"]))

    def test_unhardened_child_0H_1(self):
        private_keychain = self.root_private_keychain.hardened_child(0).child(1)
        self.assertEqual(str(private_keychain), str(self.private_keychains["0H/1"]))
        public_keychain = private_keychain.public_keychain()
        self.assertEqual(str(public_keychain), str(self.public_keychains["0H/1"]))
        public_keychain_2 = self.root_private_keychain.hardened_child(0).public_keychain().child(1)
        self.assertEqual(str(public_keychain), str(public_keychain_2))

    def test_5_step_derivation(self):
        private_keychain = self.root_private_keychain.hardened_child(0).child(1).hardened_child(2).child(2).child(1000000000)
        self.assertEqual(str(private_keychain), str(self.private_keychains["0H/1/2H/2/1000000000"]))
        public_keychain = private_keychain.public_keychain()
        self.assertEqual(str(public_keychain), str(self.public_keychains["0H/1/2H/2/1000000000"]))


def test_main():
    def altcoin_test_generator(coin_name):
        def generate(self):
            keypair = get_class(coin_name.title() + 'Keypair')
            private_key = self.reference['hex_private_key']
            keypair = keypair.from_private_key(private_key)

            wif_private_key = keypair.wif_pk()
            reference_wif_private_key = self.reference[(coin_name, 'wif')]
            self.assertEqual(wif_private_key, reference_wif_private_key)

            address = keypair.address()
            reference_address = self.reference[(coin_name, 'address')]
            self.assertEqual(address, reference_address)

        return generate

    # generate altcoin tests
    for coin_name in AltcoinKeypairTest.coin_names:
        test_name = 'test_%s' % coin_name
        test = altcoin_test_generator(coin_name)
        setattr(AltcoinKeypairTest, test_name, test)

    test_support.run_unittest(
        MerkleTest,
        BitcoinUncompressedPublicKeyTest,
        BitcoinCompressedPublicKeyTest,
        BitcoinPublicKeyCreationTest,
        BitcoinPrivateKeyTest,
        BitcoinPrivateKeyToPublicKeyTest,
        BitcoinKeypairTest,
        # AltcoinKeypairTest,
        BitcoinBrainWalletKeypairTest,
        BitcoinKeypairFromWIFTest,
        RandomBitcoinKeypairsTest,
        BitcoinB58CheckTest,
        BitcoinFormatCheckTest,
        SequentialWalletTest,
        KeychainTest
    )


def test_transactions():
    test_support.run_unittest(
        ServicesGetUnspentsTest,
        TransactionNetworkFunctionsTest,
        ServicesSendTransactionTest,
        ServicesSendOpReturnTransactionTest
    )

if __name__ == '__main__':
    test_main()
    # test_transactions()
