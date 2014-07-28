# -*- coding: utf-8 -*-
"""
	coinrpc
	~~~~~

	:copyright: (c) 2014 by Halfmoon Labs 
	:license: MIT, see LICENSE for more details.
"""

from setuptools import setup

setup(
	name='coinrpc',
	version='0.1.0',
	url='https://github.com/halfmoonlabs/coinrpc',
	license='MIT',
	author='Muneeb Ali (@muneeb) and Ibrahim Ahmed',
	author_email='hello@halfmoonlabs.com',
	description="Bitcoind and Namecoind python-rpc and Flask API",
	packages=['coinrpc'],
	zip_safe=False,
	keywords = ['python', 'bitcoin', 'namecoin', 'rpc'],
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
)