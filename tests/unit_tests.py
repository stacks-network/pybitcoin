# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, traceback, unittest, string
from test import test_support

from coinkit import *

get_class = lambda x: globals()[x]

try:
	with open('tests/secrets.json', 'r') as f:
		SECRETS = json.loads(f.read())
except:
	traceback.print_exc()

def equality_test_generator(a, b):
	def test(self):
		self.assertEqual(a, b)
	return test

def altcoin_test_generator(coin_name):
	def test(self):
		keypair = get_class(coin_name.title() + 'Keypair')
		private_key = self.reference['hex_private_key']
		keypair = keypair.from_private_key(private_key)

		wif_private_key = keypair.wif_pk()
		reference_wif_private_key = self.reference[(coin_name, 'wif')]
		self.assertEqual(wif_private_key, reference_wif_private_key)
		
		address = keypair.address()
		reference_address = self.reference[(coin_name, 'address')]
		self.assertEqual(address, reference_address)

	return test

_reference_info = {
	'passphrase': 'correct horse battery staple',
	'bin_private_key': '\xc4\xbb\xcb\x1f\xbe\xc9\x9de\xbfY\xd8\\\x8c\xb6.\xe2\xdb\x96?\x0f\xe1\x06\xf4\x83\xd9\xaf\xa7;\xd4\xe3\x9a\x8a',
	'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
	'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
	'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
	'wif_private_key':'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
	'address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
	'wif_version_byte': 128
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
		self.assertEqual(self.public_key.hash160(), self.reference['hex_hash160'])

	def test_hex_public_key(self):
		self.assertEqual(self.public_key.to_hex(), self.reference['hex_public_key'])

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
		self.assertEqual(self.public_key.bin_hash160(), self.reference['bin_hash160'])

	def test_hex_hash160(self):
		self.assertEqual(self.public_key.hash160(), self.reference['hex_hash160'])

	def test_bin_public_key(self):
		self.assertEqual(self.public_key.to_bin(), self.reference['bin_public_key'])

	def test_hex_public_key(self):
		self.assertEqual(self.public_key.to_hex(), self.reference['hex_public_key'])

class BitcoinPublicKeyCreationTest(unittest.TestCase):
	def setUp(self):
		self.address_compressed = '14Q8uVAX29RUMvqPGXL5sg6NiwwMRFCm8C'
		self.address_uncompressed = '1AuZor1RVzG22wqbH2sG2j5WRDZsbw1tip'

	def tearDown(self):
		pass

	def test_create_pubkey_from_hex_uncompressed_format(self):
		public_key_string = '04068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7b2832f87f683100b89c2e95314deeeacbc6409af1e36c3ae3fd8c5f2f243cfec'
		self.assertEqual(self.address_uncompressed, BitcoinPublicKey(public_key_string).address())

	def test_create_pubkey_from_bin_uncompressed_format(self):
		public_key_string = '\x04\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7\xb2\x83/\x87\xf6\x83\x10\x0b\x89\xc2\xe9S\x14\xde\xee\xac\xbcd\t\xaf\x1e6\xc3\xae?\xd8\xc5\xf2\xf2C\xcf\xec'
		self.assertEqual(self.address_uncompressed, BitcoinPublicKey(public_key_string).address())

	def test_create_pubkey_from_hex_ecdsa_format(self):
		public_key_string = '068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7b2832f87f683100b89c2e95314deeeacbc6409af1e36c3ae3fd8c5f2f243cfec'
		self.assertEqual(self.address_uncompressed, BitcoinPublicKey(public_key_string).address())

	def test_create_pubkey_from_bin_ecdsa_format(self):
		public_key_string = '\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7\xb2\x83/\x87\xf6\x83\x10\x0b\x89\xc2\xe9S\x14\xde\xee\xac\xbcd\t\xaf\x1e6\xc3\xae?\xd8\xc5\xf2\xf2C\xcf\xec'
		self.assertEqual(self.address_uncompressed, BitcoinPublicKey(public_key_string).address())

	def test_create_pubkey_from_hex_compressed_format(self):
		public_key_string = '02068fd9d47283fb310e6dfb66b141dd78fbabc76d073d48cddc770ffb2bd262d7'
		self.assertEqual(self.address_compressed, BitcoinPublicKey(public_key_string).address())

	def test_create_pubkey_from_bin_compressed_format(self):
		public_key_string = '\x02\x06\x8f\xd9\xd4r\x83\xfb1\x0em\xfbf\xb1A\xddx\xfb\xab\xc7m\x07=H\xcd\xdcw\x0f\xfb+\xd2b\xd7'
		self.assertEqual(self.address_compressed, BitcoinPublicKey(public_key_string).address())

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
		self.private_key_from_wif = BitcoinPrivateKey(self.reference['wif_private_key'])
		self.assertEqual(self.private_key.to_hex(), self.private_key_from_wif.to_hex())

	def test_hex_private_key(self):
		self.assertEqual(self.private_key.to_hex(), self.reference['hex_private_key'])

	def test_wif_private_key(self):
		self.assertEqual(self.private_key.to_wif(), self.reference['wif_private_key'])

class BitcoinKeypairTest(unittest.TestCase):
	reference = _reference_info

	def setUp(self):
		self.keypair = BitcoinKeypair(self.reference['hex_private_key'])

	def tearDown(self):
		pass

	def test_hex_private_key(self):
		self.assertEqual(self.keypair.private_key(), self.reference['hex_private_key'])

	def test_wif_private_key(self):
		self.assertEqual(self.keypair.wif_pk(), self.reference['wif_private_key'])

	def test_address(self):
		self.assertEqual(self.keypair.address(), self.reference['address'])

	def test_hex_hash160(self):
		self.assertEqual(self.keypair.hash160(), self.reference['hex_hash160'])

	def test_public_key(self):
		self.assertEqual(self.keypair.public_key(), self.reference['hex_public_key'])

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
		('bitcoin', 'wif'):'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
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
		self.keypair = BitcoinKeypair.from_passphrase(self.reference['passphrase'])

	def test_passphrase(self):
		self.assertEqual(self.keypair.passphrase(), self.reference['passphrase'])

	def test_random_passphrase_length(self):
		random_keypair = BitcoinKeypair.from_passphrase()
		self.assertTrue(len(random_keypair.passphrase().split()) > 1)

class BitcoinKeypairFromWIFTest(BitcoinKeypairTest):
	def setUp(self):
		BitcoinKeypairTest.setUp(self)
		self.keypair = BitcoinKeypair.from_private_key(self.reference['wif_private_key'])

class RandomBitcoinKeypairsTest(unittest.TestCase):
	def setUp(self):
		self.keypair = BitcoinKeypair()
		self.brainwallet_keypair = BitcoinKeypair.from_passphrase()

	def tearDown(self):
		pass

	def test_keypair(self):
		#self.assertTrue(is_256bit_hex_string(self.keypair.private_key()))
		#self.assertTrue(is_wif_pk(self.keypair.wif_pk()))
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
		wif_private_key = b58check_encode(bin_private_key, version_byte=self.reference['wif_version_byte'])
		self.assertEqual(self.reference['wif_private_key'], wif_private_key)
		bin_private_key_verification = b58check_decode(wif_private_key)
		self.assertEqual(bin_private_key_verification, bin_private_key)

	def test_b58check_unpack_then_encode(self):
		version_byte, bin_private_key, checksum = b58check_unpack(self.reference['wif_private_key'])
		self.assertTrue(ord(version_byte) == self.reference['wif_version_byte'])
		wif_private_key = b58check_encode(bin_private_key, version_byte=ord(version_byte))
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
		self.assertTrue(is_256bit_hex_string(self.reference['hex_private_key']))

class SequentialWalletTest(unittest.TestCase):
	reference = {
		'passphrase': 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall',
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
		self.assertEqual(self.reference['bitcoin_keypair_1']['address'], bitcoin_keypair_1.address())
		self.assertEqual(bitcoin_keypair_1.passphrase(), self.reference['passphrase'] + ' bitcoin1')

class ServicesGetUnspentsTest(unittest.TestCase):
	def setUp(self):
		self.address = '1E1PHi525xnHvSU4BqnV8aqwZwN8zoaHFv'
		self.total_unspent_value = 55366270
		self.unspents_dict = {
			'691d1645dc6f9431fe2ef414aaa88887efb5fed9354bf53ed01349595bf725ed': {
				'script_hex': '76a9148eac3d867e1f92f47da40217c3cbd3d75d05701388ac',
				'output_index': 1,
				'transaction_hash': '691d1645dc6f9431fe2ef414aaa88887efb5fed9354bf53ed01349595bf725ed',
				'confirmations': 6146,
				'value': 55366270
			}
		}

	def tearDown(self):
		pass

	def compare_unspents(self, unspents):
		for unspent in unspents:
			if unspent['transaction_hash'] in self.unspents_dict:
				ref_unspent = self.unspents_dict[unspent['transaction_hash']]
				self.assertEqual(unspent['transaction_hash'], ref_unspent['transaction_hash'])
				self.assertEqual(unspent['output_index'], ref_unspent['output_index'])
				self.assertEqual(unspent['script_hex'], ref_unspent['script_hex'])
				self.assertEqual(unspent['value'], ref_unspent['value'])
			else:
				continue

	def compare_total_value(self, unspents):
		total_value = sum([u['value'] for u in unspents])
		self.assertEqual(total_value, self.total_unspent_value)

	def test_blockchain_info_get_unspents(self):
		blockchain_client = BlockchainInfoClient(SECRETS['blockchain_api_key'])
		unspents = get_unspents(self.address, blockchain_client)
		self.compare_total_value(unspents)
		self.compare_unspents(unspents)

	def test_chain_com_get_unspents(self):
		blockchain_client = ChainComClient(SECRETS['chain_api_id'], SECRETS['chain_api_secret'])
		unspents = transactions.get_unspents(self.address, blockchain_client)
		self.compare_total_value(unspents)
		self.compare_unspents(unspents)

	def test_bitcoind_get_unspents(self):
		blockchain_client = BitcoindClient(SECRETS['rpc_username'], SECRETS['rpc_password'])
		unspents = transactions.get_unspents(self.address, blockchain_client)
		self.compare_total_value(unspents)
		self.compare_unspents(unspents)

class SendNamecoinTransactionTest(unittest.TestCase):
	def setUp(self):
		self.recipient_address = 'NKUDoWmJevpguXZn9fT37zRub4uS2mrqba'
		self.private_key = NamecoinPrivateKey(SECRET['namecoin_private_key'])
		self.namecoind_client = BitcoindClient(SECRETS['rpc_username'],
			SECRETS['rpc_password'], port=8336, version_byte=52)

	def tearDown(self):
		pass

	def test_namecoin_build_transaction(self):
		unspents = get_unspents(recipient_address, self.namecoind_client)
		signed_tx = make_send_to_address_tx(recipient_address, 1000000,
			private_key, self.namecoind_client)
		resp = broadcast_transaction(signed_tx, self.namecoind_client)
		self.assertTrue(resp.get('success'))

class ServicesSendTransactionTest(unittest.TestCase):
	def setUp(self):
		self.recipient_address = '1EEwLZVZMc2EhMf3LXDARbp4mA3qAwhBxu'
		self.private_key = BitcoinPrivateKey(SECRETS["private_key"])
		self.send_amount = 1000
		
		self.chain_com_client = ChainComClient(SECRETS['chain_api_id'],
			SECRETS['chain_api_secret'])
		self.blockchain_info_client = BlockchainInfoClient(
			SECRETS['blockchain_api_key'])
		self.bitcoind_client = BitcoindClient(SECRETS['rpc_username'],
			SECRETS['rpc_password'])

		self.signed_tx = make_send_to_address_tx(self.recipient_address, self.send_amount,
			self.private_key, self.chain_com_client)

	def tearDown(self):
		pass

	def broadcast_with_client(self, tx, blockchain_client):
		return broadcast_transaction(tx, blockchain_client)

	def send_to_address_with_client(self, blockchain_client):
		return send_to_address(self.recipient_address, 1000, self.private_key, blockchain_client)

	def test_send_transaction_chain_com(self):
		resp = self.broadcast_with_client(self.signed_tx, self.chain_com_client)
		self.assertTrue(resp.get('success'))

	def test_send_transaction_blockchain_info(self):
		resp = self.broadcast_with_client(self.signed_tx, self.blockchain_info_client)
		self.assertTrue(resp.get('success'))

	def test_send_transaction_bitcoind(self):
		resp = self.broadcast_with_client(self.signed_tx, self.bitcoind_client)
		self.assertTrue(resp.get('success'))
	
	"""
	def test_build_transaction(self):
		signed_tx = make_send_to_address_tx(recipient_address, 1000, private_key, blockchain_client)
		#print signed_tx
		self.assertTrue(True)
	"""

class ServicesSendOpReturnTransactionTest(unittest.TestCase):
	def setUp(self):
		self.private_key = SECRETS['private_key_2']

		self.chain_com_client = ChainComClient(SECRETS['chain_api_id'],
			SECRETS['chain_api_secret'])
		self.blockchain_info_client = BlockchainInfoClient(
			SECRETS['blockchain_api_key'])
		self.bitcoind_client = BitcoindClient(SECRETS['rpc_username'],
			SECRETS['rpc_password'])

		self.fee = 10000

	def tearDown(self):
		pass

	def run_op_return_tx_building(self, data, blockchain_client, format='bin'):
		return make_op_return_tx(data, self.private_key, blockchain_client, fee=self.fee, format=format)

	def run_tx_broadcasting(self, tx, blockchain_client):
		return broadcast_transaction(tx, blockchain_client)

	"""
	def run_data_embedding(self, data, blockchain_client):
		resp = embed_data_in_blockchain(data, self.private_key,
			blockchain_client, format='hex', fee=100000)
		return resp
	"""

	def test_hex_op_return_tx(self):
		data = '00'*40
		signed_tx = self.run_op_return_tx_building(data, self.chain_com_client, format='hex')
		resp = self.run_tx_broadcasting(signed_tx, self.chain_com_client)
		self.assertTrue(resp.get('success'))

	"""
	def test_short_hex_op_return_tx(self):
		resp = embed_data('0'*2)
		self.assertTrue(resp.get('success'))

	def test_bin_op_return_tx(self):
		resp = embed_data("Hello, Blockchain!")
		self.assertTrue(resp.get('success'))
	"""

def test_main():

	# generate altcoin tests
	for coin_name in AltcoinKeypairTest.coin_names:
		test_name = 'test_%s' % coin_name
		test = altcoin_test_generator(coin_name)
		setattr(AltcoinKeypairTest, test_name, test)

	test_support.run_unittest(
		BitcoinUncompressedPublicKeyTest,
		BitcoinCompressedPublicKeyTest,
		BitcoinPublicKeyCreationTest,
		BitcoinPrivateKeyTest,
		BitcoinPrivateKeyToPublicKeyTest,
		BitcoinKeypairTest,
		#AltcoinKeypairTest,
		#BitcoinBrainWalletKeypairTest,
		#BitcoinKeypairFromWIFTest,
		#RandomBitcoinKeypairsTest,
		BitcoinB58CheckTest,
		BitcoinFormatCheckTest,
		#SequentialWalletTest,
	)

def test_transactions():
	test_support.run_unittest(
		ServicesGetUnspentsTest,
		#ServicesSendTransactionTest,
		#ServicesSendOpReturnTransactionTest
	)

if __name__ == '__main__':
    test_main()
    #test_transactions()

