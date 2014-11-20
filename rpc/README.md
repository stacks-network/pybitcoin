coinrpc
=======

Coinrpc is a python library for RPC calls to namecoind and bitcoind. Under the hood it uses [AuthProxy](https://github.com/jgarzik/python-bitcoinrpc). The main goal of coinrpc is to make it easier to perform common operations using namecoind/bitcoind.  

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
