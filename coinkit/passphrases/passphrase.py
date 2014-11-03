# -*- coding: utf-8 -*-
"""
    Coinkit
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import random, math
from .english_words import english_words_bip39, english_words_wiktionary, \
    english_words_google

system_random = random.SystemRandom()

def get_wordlist(language, word_source):
    """ Takes in a language and a word source and returns a matching wordlist,
        if it exists.
        Valid languages: ['english']
        Valid word sources: ['bip39', 'wiktionary', 'google']
    """
    try:
        wordlist_string = eval(language + '_words_' + word_source)
    except NameError:
        raise Exception("No wordlist could be found for the word source and language provided.")
    wordlist = wordlist_string.split(',')
    return wordlist

def get_num_words_required_for_entropy(bits_of_entropy, wordlist):
    """ Gets the number of words randomly selected from a given wordlist that
        would result in the number of bits of entropy specified.
    """
    entropy_per_word = math.log(len(wordlist))/math.log(2)
    num_words = int(math.ceil(bits_of_entropy/entropy_per_word))
    return num_words

def pick_random_words_from_wordlist(wordlist, num_words_to_choose):
    """ Picks words randomly from a wordlist.
    """
    return [system_random.choice(wordlist) for i in range(num_words_to_choose)]

def create_passphrase_with_num_words(num_words, language='english',
                                  word_source='bip39'):
    """ Creates a passphrase of a certain wordlength.
    """
    wordlist = get_wordlist(language, word_source)
    return ' '.join(pick_random_words_from_wordlist(wordlist, num_words))

def create_passphrase_with_entropy_level(bits_of_entropy, language='english',
                                      word_source='bip39'):
    """ Creates a passphrase that has a certain number of bits of entropy.
    """
    wordlist = get_wordlist(language, word_source)
    num_words = get_num_words_required_for_entropy(bits_of_entropy, wordlist)
    return ' '.join(pick_random_words_from_wordlist(wordlist, num_words))

def create_simple_passphrase():
    return create_passphrase_with_num_words(num_words=4, word_source='bip39')

def create_128bit_passphrase():
    return create_passphrase_with_entropy_level(128, word_source='bip39')

def create_160bit_passphrase():
    return create_passphrase_with_entropy_level(160, word_source='wiktionary')

def create_256bit_passphrase():
    return create_passphrase_with_entropy_level(256, word_source='wiktionary')

