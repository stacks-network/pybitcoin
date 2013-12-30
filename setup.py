"""
Coins
==============

"""

from setuptools import setup

setup(
    name='Coins',
    version='0.1.10',
    url='https://github.com/halfmoonlabs/coins',
    license='MIT',
    author='Halfmoon Labs',
    author_email='hello@halfmoon.io',
    description='Tools for Bitcoin and other cryptocurrencies (including Litecoin, Namecoin, Peercoin, and Primecoin).',
    keywords='bitcoin btc litecoin namecoin cryptocurrency',
    packages=[
        'coins',
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
