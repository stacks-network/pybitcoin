"""
Coinkit
==============

"""

from setuptools import setup, find_packages

setup(
    name='coinkit',
    version='0.7.7',
    url='https://github.com/onenameio/coinkit',
    license='MIT',
    author='Onename (Halfmoon Labs)',
    author_email='hello@halfmoon.io',
    description='Tools for Bitcoin & other cryptocurrencies (incl. Litecoin, Namecoin, Peercoin, Primecoin, Dogecoin, Worldcoin, Megacoin, Anoncoin, Feathercoin, Terracoin, and Novacoin).',
    keywords='bitcoin btc litecoin namecoin dogecoin cryptocurrency',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'ecdsa==0.11',
        'utilitybelt>=0.2.1',
        'requests>=2.4.3',
        'pybitcointools==1.1.15',
        'python-bitcoinrpc==0.1'
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
