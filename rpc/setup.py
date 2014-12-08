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
	url='https://github.com/openname/coinrpc',
	license='MIT',
	author='Muneeb Ali (@muneeb) and Ibrahim Ahmed',
	author_email='hello@halfmoonlabs.com',
	description="Bitcoind and Namecoind python-rpc",
	packages=['coinrpc'],
	include_package_data=True,
	install_requires=['python-bitcoinrpc==0.1','commontools==0.1.0'],
	zip_safe=False,
	keywords = ['python', 'bitcoin', 'namecoin', 'rpc'],
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
)