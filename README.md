Coins
=====

Tools for Bitcoin and other cryptocurrencies.

Supported currencies:

- Litecoin
- Namecoin
- Peercoin
- Primecoin
- Testnet
- Worldcoin
- Megacoin
- Feathercoin
- Terracoin
- Novacoin
- Dogecoin
- Anoncoin
- Protoshares
- Ixcoin
- Memorycoin
- Infinitecoin
- Cryptogenic Bullion
- Quarkcoin
- Netcoin
- Earthcoin

### Standard Usage

	>>> from coins.keypair import BitcoinKeypair
	>>> k = BitcoinKeypair('c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
	>>> k.private_key()
	'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a'
	>>> k.public_key()
	'0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455'
	>>> k.wif_pk()
	'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS'
	>>> k.address()
	'1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T'

### Brain wallet keypairs

	>>> k = BitcoinKeypair().from_passphrase('correct horse battery staple')
	>>> k.passphrase()
	'correct horse battery staple'
	>>> k.address()
	'1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T'

### Randomly-generated keypairs

	>>> k1 = BitcoinKeypair()
	>>> k2 = BitcoinKeypair.from_passphrase()

### Altcoin keypairs

	>>> from coins.keypair import LitecoinKeypair, NamecoinKeypair
	>>> ltc_k = LitecoinKeypair('c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
	>>> ltc_k.address()
	'LdAPi7uXrLLmeh7u57pzkZc3KovxEDYRJq'
	>>> nmc_k = NamecoinKeypair('c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
	'NEWoeZ6gh4CGvRgFAoAGh4hBqpxizGT6gZ'

