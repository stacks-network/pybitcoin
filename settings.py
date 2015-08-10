import os

secrets_list = [
    'CHAIN_API_ID', 'CHAIN_API_SECRET', 'BITCOIN_PRIVATE_KEY', \
    'BITCOIN_PRIVATE_KEY_2', 'BITCOIND_RPC_USERNAME', 'BITCOIND_RPC_PASSWORD',
    'NAMECOIN_PRIVATE_KEY', 'BLOCKCHAIN_API_KEY', 'BLOCKCYPHER_API_KEY'
]

for env_variable in os.environ:
    if env_variable in secrets_list:
        env_value = os.environ[env_variable]
        exec(env_variable + " = \"\"\"" + env_value + "\"\"\"")