pybitcoin
=====

[![CircleCI](https://img.shields.io/circleci/project/blockstack/pybitcoin.svg)](https://circleci.com/gh/blockstack/pybitcoin)
[![PyPI](https://img.shields.io/pypi/v/pybitcoin.svg)](https://pypi.python.org/pypi/pybitcoin/)
[![PyPI](https://img.shields.io/pypi/dm/pybitcoin.svg)](https://pypi.python.org/pypi/pybitcoin/)
[![PyPI](https://img.shields.io/pypi/l/pybitcoin.svg)](https://github.com/namesystem/pybitcoin/blob/master/LICENSE)
[![Slack](http://slack.blockstack.org/badge.svg)](http://slack.blockstack.org/)

Python library with tools for Bitcoin and other cryptocurrencies.

## Usage

### Private Keys

```python
>>> from pybitcoin import BitcoinPrivateKey
>>> private_key = BitcoinPrivateKey()
>>> private_key.to_hex()
'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> private_key.to_wif()
'5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
>>> private_key_2 = BitcoinPrivateKey('91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d')
>>> print private_key.to_wif() == private_key_2.to_wif()
True
```

### Public Keys

```python
>>> public_key = private_key.public_key()
>>> public_key.to_hex()
'042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
>>> public_key_2 = BitcoinPublicKey(public_key.to_hex())
>>> print public_key.to_hex() == public_key_2.to_hex()
True
```

### Addresses

```python
>>> public_key.address()
'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'
>>> public_key.hash160()
'1e6db1e09b5e307847e5734864a79ea0113d0083'
```

### Brainwallet-based Private Keys

```python
>>> private_key = BitcoinPrivateKey.from_passphrase()
>>> private_key.passphrase()
'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
>>> private_key.to_hex()
'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> priv2 = BitcoinPrivateKey.from_passphrase(priv2.passphrase())
>>> print private_key.to_hex() == priv2.to_hex()
True
```

### Sending Transactions to Addresses

```python
>>> from pybitcoin import BlockcypherClient
>>> recipient_address = '1EEwLZVZMc2EhMf3LXDARbp4mA3qAwhBxu'
>>> blockchain_client = BlockcypherClient(BLOCKCYPHER_API_KEY)
>>> send_to_address(recipient_address, 10000, private_key.to_hex(), blockchain_client)
```

### Sending OP_RETURN Transactions

```python
>>> from pybitcoin import make_op_return_tx
>>> data = '00' * 80
>>> tx = make_op_return_tx(data, private_key.to_hex(), blockchain_client, fee=10000, format='bin')
>>> broadcast_transaction(tx, blockchain_client)
{"success": True}
```

### Altcoins

```python
>>> class NamecoinPrivateKey(BitcoinPrivateKey):
>>>     _pubkeyhash_version_byte = 52
>>> namecoin_private_key = NamecoinPrivateKey(private_key.to_hex())
>>> namecoin_private_key.to_wif()
'73zteEjenBCK7qVtG2yRPeco2TP5w93qBW5sJkxYoGYvbWwAbXv'
>>> namecoin_public_key = namecoin_private_key.public_key()
>>> namecoin_public_key.address()
'MyMFt8fQdZ6rEyDhZbe2vd19gD8gzagr7Z'
```

## Supported currencies

Litecoin, Namecoin, Peercoin, Primecoin, Testnet, Worldcoin, Megacoin, Feathercoin, Terracoin, Novacoin, Dogecoin, Anoncoin, Protoshares, Ixcoin, Memorycoin, Infinitecoin, Cryptogenic Bullion, Quarkcoin, Netcoin, Earthcoin, Reddcoin, (insert your favorite cryptocurrency here)

## Developers

**Q:** Can I contribute to pybitcoin?

**A:** Of course! Any and all are encouraged to contribute. Just fork a copy of the repo and get started on something that you think would improve the current offering.

**Q:** What should I work on?

**A:** That's up to you! For a quick project, consider adding support for a new cryptocurrency (should only require two lines of code, not including the unit tests).

Meanwhile, for something a bit more ambitious, check the issues section for outstanding feature requests.

## Notice

pybitcoin is still in beta. Developers using pybitcoin are encouraged to inspect the code for themselves and perform their own tests. We are committed to ensuring that this library behaves exactly as it is supposed to under all conditions, and have plans to ramp up our testing efforts going forward.
