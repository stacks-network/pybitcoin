rpc
=======

This directory in Bitcoinkit contains RPC calls to bitcoind and namecoind. Under the hood it uses [AuthProxy](https://github.com/jgarzik/python-bitcoinrpc). We make the following changes/additions: 

For Namecoind:

  1. Support for managing a cluster of namecoind servers
  2. Adds get_full_profile() that can fetch an Openname profile from a linked-list of key:value entries
  3. Fixes the bug where value > 520 bytes can cause a key to become unusable
  4. Logically separates name_transfer from name_update 
  5. Adds reasonable default values for certain calls e.g., 100 as timeout for unlocking wallet
  6. Adds calls for checking if a user is registered (True/False) and if a wallet is unlocked (True/False)
  7. Better error handling 
  
## Installation:

```
pip install git+ssh://git@github.com/openname/bitcoinkit.git
```

Custom namecoind/bitcoind servers can be used by setting the appropriate ENV VARIABLES (see [config.py](./config.py)) e.g., by sourcing the following scripts:

```
source <path-to-dir>/rpc/scripts/setup_namecoind.sh 
source <path-to-dir>/rpc/scripts/setup_bitcoind.sh
```

## Usage: 

```
from bitcoinkit import namecoind
print namecoind.blocks()
```
