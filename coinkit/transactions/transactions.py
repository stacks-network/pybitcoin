from ..services import blockchain_info, blockcypher_com, chain_com

def send_transaction(hex_tx, api='chain.com'):
    if api == 'blockchain.info':
        return blockchain_info.send_transaction(hex_tx)
    elif api == 'chain.com':
        return chain_com.send_transaction(hex_tx)
    else:
        raise Exception('API not supported.')

