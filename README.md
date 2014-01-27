Coinkit
=====

Tools for Bitcoin and other cryptocurrencies.

## Example Usage

### Keypairs

#### Custom keypairs

    >>> from coinkit.keypair import BitcoinKeypair
    >>> hex_private_key = '91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
    >>> keypair = BitcoinKeypair(hex_private_key)
    >>> keypair.private_key()
    '91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
    >>> keypair.public_key()
    '042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
    >>> keypair.wif_pk()
    '5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
    >>> keypair.address()
    '13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'

#### Brain wallet keypairs
    
    >>> passphrase = 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
    >>> keypair = BitcoinKeypair.from_passphrase(passphrase)
    >>> keypair.passphrase()
    'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
    >>> keypair.address()
    '13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'

#### Randomly-generated keypairs

    >>> keypair_from_random_private_key = BitcoinKeypair()
    >>> keypair_from_random_passphrase = BitcoinKeypair.from_passphrase()

#### Altcoin keypairs

    >>> from coinkit.keypair import LitecoinKeypair
    >>> litecoin_keypair = LitecoinKeypair(hex_private_key)
    >>> litecoin_keypair.address()
    'LMzqwhUFnqFLyEfMTvJkz7v1AC6v8N9Qcd'

### Wallets

#### Sequential Deterministic Wallets

    >>> from coinkit.wallet import SDWallet
    >>> from coinkit.keypair import BitcoinKeypair
    >>> passphrase = 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
    >>> wallet = SDWallet(passphrase)
    >>> bitcoin_keypair_1 = wallet.keypair(1, BitcoinKeypair)
    >>> bitcoin_keypair_1.passphrase()
    'shepherd mais pack rate enamel horace diva filesize maximum really roar mall bitcoin1'
    >>> bitcoin_keypair_1.address()
    '1DS2vmsqTwtXp1DfmDHi55Aqc6w4LBUC9k'

### Utilities

#### Generating random passphrases

    >>> from coinkit.passphrase import random_160bit_passphrase
    >>> random_160bit_passphrase()
    'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'

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
