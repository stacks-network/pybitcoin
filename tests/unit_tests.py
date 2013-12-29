import unittest
from test import test_support

from coins.addresses import BitcoinAddress

class BitcoinAddressTest(unittest.TestCase):

	def setUp(self):
		self.reference = {
			'passphrase': 'correct horse battery staple',
			'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
			'wif_private_key':'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
			'address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
			'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
			'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
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
		BitcoinBrainWalletAddressTest,
		BitcoinAddressFromWIFTest,
		BitcoinUtilsTest
	)

if __name__ == '__main__':
    test_main()
