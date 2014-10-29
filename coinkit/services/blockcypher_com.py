import json, requests, traceback

BLOCKCYPHER_API_BASE_URL = "http://api.blockcypher.com/v1/btc/main"

def format_unspents(unspents):
    return [{
        "transaction_hash": s["tx_hash"],
        "output_index": s["tx_output_n"],
        "value": s["value"],
        "confirmations": s["confirmations"]
        }
        for s in unspents
    ]

def get_unspents(address):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    url = BLOCKCYPHER_API_BASE_URL + "/addrs/" + address + "?unspentOnly=true"

    r = requests.get(url)
    try:
        data = r.json()
    except ValueError, e:
        raise Exception('Invalid response from API.')

    unspents = []
    if "txrefs" in data:
        unspents.extend(data["txrefs"])
    if "unconfirmed_txrefs" in data:
        unspents.extend(data["unconfirmed_txrefs"])

    return format_unspents(unspents)

class BlockcypherClient():
    def __init__(self):
        pass

    def auth(self):
        return None

    def get_unspents(self, address):
        return get_unspents(address)

if __name__ == '__main__':
    pass

