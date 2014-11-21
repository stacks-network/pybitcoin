coinrpc
=======

Coinrpc is a python library for RPC calls to namecoind and bitcoind. Under the hood it uses [AuthProxy](https://github.com/jgarzik/python-bitcoinrpc). Coinrpc makes the following changes/additions to directly using the underlying RPC: 

For Namecoind:

  1. Adds get_full_profile() that can fetch an Openname profile from a linked-list of key:value entries
  2. Fixes the bug where value > 520 bytes can cause a key to become unusable
  3. Logically separates name_transfer from name_update 
  4. Adds reasonable default values for certain calls e.g., 100 as timeout for unlocking wallet
  5. Adds calls for checking if a user is registered (True/False) and if a wallet is unlocked (True/False)
  6. Better error handling 
  7. Support of managing a cluster of namecoind servers (coming soon)

## Installation:

```
pip install git+ssh://git@github.com/onenameio/coinrpc.git
```

By default bitcoind is turned off and the configuration of a public namecoind server is used. Custom namecoind/bitcoind servers can be used by setting the appropriate ENV VARIABLES (see [config.py](coinrpc/config.py)) e.g., by sourcing the following scripts:

```
source <path-to-dir>/coinrpc/scripts/setup_namecoind.sh 
source <path-to-dir>/coinrpc/scripts/setup_bitcoind.sh
```

## Usage: 

```
from coinrpc import namecoind
print namecoind.blocks()
```
