"""
Coins
==============

"""

from setuptools import setup

setup(
    name='Coins',
    version='0.1.8',
    url='https://github.com/halfmoonlabs/coins',
    license='MIT',
    author='Halfmoon Labs',
    author_email='hello@halfmoon.io',
    description='Bitcoin, Litecoin, Namecoin, Peercoin, & Primecoin tools.',
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
    ],
)
