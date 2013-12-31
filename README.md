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

	from coins.address import BitcoinAddress, LitecoinAddress, NamecoinAddress

	a = BitcoinAddress()

### Randomly-generated addresses

	a = BitcoinAddress()

	print a
	print a.wif_private_key()
	print a.secret_exponent()

### Custom addresses

	a1 = BitcoinAddress('c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
	a2 = BitcoinAddress.from_wif('5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS')

	assert(a1.secret_exponent() == 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a')
	assert(a2.wif_private_key() == '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS')

### Brain wallet addresses

	a = BitcoinAddress().from_passphrase()

	print a.passphrase()

	a = BitcoinAddress().from_passphrase('correct horse battery staple')

	assert(a.passphrase() == 'correct horse battery staple')

### Altcoin addresses

	ba = BitcoinAddress()
	la = LitecoinAddress()
	na = NamecoinAddress()


