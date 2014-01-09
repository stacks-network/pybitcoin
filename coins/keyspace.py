import re

def int_to_hex(i):
    return re.sub(r'^0x|L$', '', hex(i))

def int_to_string(integer, keyspace_chars):
    """ Turn a positive integer into a string. """
    if not integer > 0:
        raise ValueError('integer must be > 0')
    output = ""
    while integer > 0:
        integer, digit = divmod(integer, len(keyspace_chars))
        output += keyspace_chars[digit]
    return output[::-1]

def string_to_int(string, keyspace_chars):
    """ Turn a string into a positive integer. """
    output = 0
    for char in string:
        output = output * len(keyspace_chars) + keyspace_chars.index(char)
    return output

def change_keyspace(string, original_keyspace, target_keyspace):
    """ Convert a string from one keyspace to another. """
    assert isinstance(string, str)
    intermediate_integer = string_to_int(string, original_keyspace)
    output_string = int_to_string(intermediate_integer, target_keyspace)
    return output_string