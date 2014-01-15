Coinkit
=====

Tools for Bitcoin and other cryptocurrencies.

## Example Usage

### Custom keypairs

	>>> from coinkit.keypair import BitcoinKeypair
	>>> hex_private_key = '91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
	>>> k = BitcoinKeypair(hex_private_key)
	>>> k.private_key()
	'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
	>>> k.public_key()
	'042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
	>>> k.wif_pk()
	'5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
	>>> k.address()
	'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'

### Brain wallet keypairs
	
	>>> passphrase = 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
	>>> k = BitcoinKeypair().from_passphrase(passphrase)
	>>> k.passphrase()
	'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
	>>> k.address()
	'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'

### Randomly-generated keypairs

	>>> k1 = BitcoinKeypair()
	>>> k2 = BitcoinKeypair.from_passphrase()

### Altcoin keypairs

	>>> from coinkit.keypair import LitecoinKeypair
	>>> ltc_k = LitecoinKeypair(hex_private_key)
	>>> ltc_k.address()
	'LMzqwhUFnqFLyEfMTvJkz7v1AC6v8N9Qcd'

## Supported currencies

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
