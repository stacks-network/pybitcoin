# -*- coding: utf-8 -*-
"""
    pybitcoin
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

_errors = {
    "EXPONENT_OUTSIDE_CURVE_ORDER": (
        "Secret exponent is outside of the"
        "valid range. Must be >= 1 and < the curve order."),
    "PHRASE_YIELDS_INVALID_EXPONENT": (
        "Invalid passphrase. The hash of this "
        "passphrase exceeds the curve order. Please try another passphrase."),
    "MUST_BE_VALID_PRIVKEY_FORMAT": (
        "Format must be bin, hex, wif, or "
        "b58check."),
    "MUST_BE_VALID_PUBKEY_FORMAT": ("Format must be bin or hex"),
    "MUST_BE_VALID_HASH160_FORMAT": (
        "format must be bin, hex or "
        "b58check."),
    "NOT_A_BRAIN_WALLET": (
        "No passphrase! This isn't a brain wallet address!"),
    "MUST_BE_A_HEX_STRING": ("Must be a hex string"),
    "IMPROPER_PUBLIC_KEY_FORMAT": ("Public key is not in proper format"),
}
