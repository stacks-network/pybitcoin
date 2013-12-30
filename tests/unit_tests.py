import unittest
from test import test_support

from coins.address import *

class BitcoinAddressTest(unittest.TestCase):

	def setUp(self):
		self.reference = {
			'passphrase': 'correct horse battery staple',
			'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
			'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
			'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
			'wif_private_key':'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
			'address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
		}
		self.address = BitcoinAddress.from_secret_exponent(self.reference['hex_private_key'])

	def tearDown(self):
		pass

	def test_hex_private_key(self):
		self.assertTrue(self.address.hex_private_key() == self.reference['hex_private_key'])

	def test_wif_private_key(self):
		self.assertTrue(self.address.wif_private_key() == self.reference['wif_private_key'])

	def test_address(self):
		self.assertTrue(str(self.address) == self.reference['address'])

	def test_hex_hash160(self):
		self.assertTrue(self.address.hex_hash160() == self.reference['hex_hash160'])

	def test_public_key(self):
		self.assertTrue(self.address.hex_public_key() == self.reference['hex_public_key'])

get_class = lambda x: globals()[x]

class AltcoinAddressTest(unittest.TestCase):
	def setUp(self):
		self.reference = {
			'passphrase': 'correct horse battery staple',
			'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
			'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
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
		}
		self.coin_names = [
			'bitcoin', 'litecoin', 'namecoin', 'peercoin', 'primecoin',
			'dogecoin', 'worldcoin', 'feathercoin', 'terracoin', 'novacoin',
			'testnet', 'protoshares', 'memorycoin', 'quarkcoin', 'infinitecoin',
			'cryptogenicbullion', 'ixcoin'
		]

		for coin_name in self.coin_names:
			address_class = get_class(coin_name.title() + 'Address')
			secret_exponent = self.reference['hex_private_key']
			address = address_class.from_secret_exponent(secret_exponent)
			setattr(self, (coin_name + '_address'), address)
		
	def tearDown(self):
		pass

	def test_wif_private_key(self):
		for coin_name in self.coin_names:
			private_key = getattr(self, coin_name + '_address').private_key()
			reference_private_key = self.reference[(coin_name, 'wif')]
			self.assertTrue(private_key == reference_private_key)
		
	def test_address(self):
		for coin_name in self.coin_names:
			address = str(getattr(self, coin_name + '_address'))
			reference_address = self.reference[(coin_name, 'address')]
			self.assertTrue(address == reference_address)

class BitcoinBrainWalletAddressTest(BitcoinAddressTest):
	def setUp(self):
		BitcoinAddressTest.setUp(self)
		self.address = BitcoinAddress.from_passphrase(self.reference['passphrase'], num_words=4)

	def test_passphrase(self):
		self.assertTrue(self.address.passphrase() == self.reference['passphrase'])

class BitcoinAddressFromWIFTest(BitcoinAddressTest):
	def setUp(self):
		BitcoinAddressTest.setUp(self)
		self.address = BitcoinAddress.from_wif_private_key(self.reference['wif_private_key'])

from coins.utils import b58check_encode, b58check_decode, b58check_unpack, \
	is_wif_private_key, is_hex_private_key

class BitcoinUtilsTest(unittest.TestCase):
	def setUp(self):
		self.hex_private_key = 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a'
		self.wif_private_key = '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS'
		self.version_byte = 128

	def tearDown(self):
		pass

	def test_b58check_encode_then_decode(self):
		bin_private_key = self.hex_private_key.decode('hex')
		wif_private_key = b58check_encode(bin_private_key, version_byte=self.version_byte)
		self.assertTrue(self.wif_private_key == wif_private_key)
		bin_private_key_verification = b58check_decode(wif_private_key)
		self.assertTrue(bin_private_key_verification == bin_private_key)

	def test_b58check_unpack_then_encode(self):
		version_byte, bin_private_key, checksum = b58check_unpack(self.wif_private_key)
		self.assertTrue(ord(version_byte) == self.version_byte)
		wif_private_key = b58check_encode(bin_private_key, version_byte=ord(version_byte))
		self.assertTrue(self.wif_private_key == wif_private_key)

	def test_is_wif_private_key(self):
		self.assertTrue(is_wif_private_key(self.wif_private_key))

	def test_is_hex_private_key(self):
		self.assertTrue(is_hex_private_key(self.hex_private_key))

def test_main():
	test_support.run_unittest(
		BitcoinAddressTest,
		AltcoinAddressTest,
		BitcoinBrainWalletAddressTest,
		BitcoinAddressFromWIFTest,
		BitcoinUtilsTest
	)

if __name__ == '__main__':
    test_main()
