#!/usr/bin/env python
"""
pybitcoin
==============

"""

from setuptools import setup, find_packages

setup(
    name='pybitcoin',
    version='0.9.9',
    url='https://github.com/blockstack/pybitcoin',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description="""Library for Bitcoin & other cryptocurrencies. Tools are provided for blockchain transactions, RPC calls, and private keys, public keys, and addresses.""",
    keywords='bitcoin btc litecoin namecoin dogecoin cryptocurrency',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'requests>=2.4.3',
        'ecdsa>=0.13',
        'commontools==0.1.0',
        'utilitybelt>=0.2.6',
        'python-bitcoinrpc==0.1',
        'keychain>=0.1.4',
        'bitcoin>=1.1.42'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
