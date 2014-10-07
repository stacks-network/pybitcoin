Coinkit
=====

[![Latest Version](https://pypip.in/version/coinkit/badge.svg)](https://pypi.python.org/pypi/coinkit/)
[![Downloads](https://pypip.in/download/coinkit/badge.svg)](https://pypi.python.org/pypi/coinkit/)
[![License](https://pypip.in/license/coinkit/badge.svg)](https://pypi.python.org/pypi/coinkit>/)

Python library with tools for Bitcoin and other cryptocurrencies.

## Usage

### Private Keys

```python
>>> from coinkit import BitcoinPrivateKey
>>> priv = BitcoinPrivateKey()
>>> priv.to_hex()
'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> priv.to_wif()
'5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
>>> priv2 = BitcoinPrivateKey('91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d')
>>> print priv.to_wif() == priv2.to_wif()
True
```

### Public Keys

```python
>>> pub = priv.public_key()
>>> pub.to_hex()
'042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
>>> pub2 = BitcoinPublicKey(pub.to_hex())
>>> print pub.to_hex() == pub2.to_hex()
True
```

### Addresses

```python
>>> pub.address()
'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'
>>> pub.hash160()
'1e6db1e09b5e307847e5734864a79ea0113d0083'
```

### Brainwallet-based Private Keys

```python
>>> priv = BitcoinPrivateKey.from_passphrase()
>>> priv.passphrase()
'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
>>> priv.to_hex()
'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> priv2 = BitcoinPrivateKey.from_passphrase(priv2.passphrase())
>>> print priv.to_hex() == priv2.to_hex()
True
```

### Altcoins

```python
>>> class NamecoinPrivateKey(BitcoinPrivateKey):
>>>     _pubkeyhash_version_byte = 52
>>> namecoin_priv = NamecoinPrivateKey(priv.to_hex())
>>> namecoin_priv.to_wif()
'73zteEjenBCK7qVtG2yRPeco2TP5w93qBW5sJkxYoGYvbWwAbXv'
>>> namecoin_pub = namecoin_priv.public_key()
>>> namecoin_pub.address()
'MyMFt8fQdZ6rEyDhZbe2vd19gD8gzagr7Z'
```

## Supported currencies

Litecoin, Namecoin, Peercoin, Primecoin, Testnet, Worldcoin, Megacoin, Feathercoin, Terracoin, Novacoin, Dogecoin, Anoncoin, Protoshares, Ixcoin, Memorycoin, Infinitecoin, Cryptogenic Bullion, Quarkcoin, Netcoin, Earthcoin, Reddcoin

## Developers

**Q:** Can I contribute to Coinkit?

**A:** Of course! Any and all are encouraged to contribute. Just fork a copy of the repo and get started on something that you think would improve the current offering.

**Q:** What should I work on?

**A:** That's up to you! For a quick project, consider adding support for a new cryptocurrency (should only require two lines of code, not including the unit tests).

Meanwhile, for something a bit more ambitious, check the issues section for outstanding feature requests.

## Notice

Coinkit is still in beta. Developers using Coinkit are encouraged to inspect the code for themselves and perform their own tests. We are committed to ensuring that this library behaves exactly as it is supposed to under all conditions, and have plans to ramp up our testing efforts going forward.
