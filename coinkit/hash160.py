import binascii, hashlib
from .formatcheck import is_hex

from .b58check import b58check_encode
from .errors import _errors

def bin_hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

class Hash160():
    def __init__(self, public_key, version_byte=0):
        if is_hex(public_key):
            binary_public_key = binascii.unhexlify(public_key)
        else:
            binary_public_key = public_key
        self._binary_value = bin_hash160(binary_public_key)
        self._version_byte = version_byte
    
    def to_bin(self):
        return self._binary_value
    
    def to_hex(self):
        return binascii.hexlify(self.to_bin())
    
    def to_b58check(self):
        return b58check_encode(self.to_bin(), version_byte=self._version_byte)
    
    def address(self):
        return self.to_b58check()
    
    def __str__(self):
        return self.to_hex()

    def __repr__(self):
        return self.to_hex()

