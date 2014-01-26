from .keypair import *
from .passphrase import random_256bit_passphrase, random_160bit_passphrase

class DeterministicWallet():
    def __init__(self, passphrase=None, min_words=12):
        """ Create keypair from a passphrase input (a brain wallet keypair)."""
        if passphrase:
            if not len(passphrase.split()) >= min_words:
                raise Exception("Warning! Passphrase must be at least " + str(min_words) + " words.")
        else:
            passphrase = random_160bit_passphrase()

        self._passphrase = passphrase
    
    def passphrase(self):
        return self._passphrase

    def keypair(self, i, keypair_class):
        currency_name = keypair_class.__name__.lower().replace('keypair', '')

        k = keypair_class.from_passphrase(
            self._passphrase + " " + currency_name + str(i))

        return k
