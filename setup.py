"""
Coins
==============

"""

from setuptools import setup

setup(
    name='coinkit',
    version='0.3.0',
    url='https://github.com/halfmoonlabs/coinkit',
    license='MIT',
    author='Halfmoon Labs',
    author_email='hello@halfmoon.io',
    description='Tools for Bitcoin & other cryptocurrencies (incl. Litecoin, Namecoin, Peercoin, Primecoin, Dogecoin, Worldcoin, Megacoin, Anoncoin, Feathercoin, Terracoin, and Novacoin).',
    keywords='bitcoin btc litecoin namecoin peercoin primecoin cryptocurrency',
    packages=[
        'coinkit',
    ],
    zip_safe=False,
    install_requires=[
        'ecdsa>=0.10',
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
