### Keypairs

#### Random keypairs

```python
>>> from pybitcoin import BitcoinKeypair
>>> keypair = BitcoinKeypair()
>>> keypair.private_key()
'91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> keypair.public_key()
'042c6b7e6da7633c8f226891cc7fa8e5ec84f8eacc792a46786efc869a408d29539a5e6f8de3f71c0014e8ea71691c7b41f45c083a074fef7ab5c321753ba2b3fe'
>>> keypair.wif_pk()
'5JvBUBPzU42Y7BHD7thTnySXQXMk8XEJGGQGcyBw7CCkw8RAH7m'
>>> keypair.address()
'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'
```

#### Custom keypairs

```python
>>> hex_private_key = '91149ee24f1ee9a6f42c3dd64c2287781c8c57a6e8e929c80976e586d5322a3d'
>>> keypair = BitcoinKeypair(hex_private_key)
```

### Utilities

#### Random passphrases

```python
>>> from pybitcoin import random_160bit_passphrase
>>> random_160bit_passphrase()
'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
```

#### Random brain wallet keypairs

```python
>>> keypair = BitcoinKeypair.from_passphrase()
>>> keypair.passphrase()
'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
>>> keypair.address()
'13mtgVARiB1HiRyCHnKTi6rEwyje5TYKBW'
```

#### Custom brain wallet keypairs

```python
>>> passphrase = 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
>>> keypair = BitcoinKeypair.from_passphrase(passphrase)
```

#### Altcoin keypairs

```python
>>> from pybitcoin import LitecoinKeypair
>>> litecoin_keypair = LitecoinKeypair()
>>> litecoin_keypair.address()
'LMzqwhUFnqFLyEfMTvJkz7v1AC6v8N9Qcd'
```

### Wallets

#### Sequential Deterministic Wallets

```python
>>> from pybitcoin import SDWallet, BitcoinKeypair
>>> passphrase = 'shepherd mais pack rate enamel horace diva filesize maximum really roar mall'
>>> wallet = SDWallet(passphrase)
>>> bitcoin_keypair_1 = wallet.keypair(1, BitcoinKeypair)
>>> bitcoin_keypair_1.passphrase()
'shepherd mais pack rate enamel horace diva filesize maximum really roar mall bitcoin1'
>>> bitcoin_keypair_1.address()
'1DS2vmsqTwtXp1DfmDHi55Aqc6w4LBUC9k'
```