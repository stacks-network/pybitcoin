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
	install_requires=['Flask==0.10.1','Jinja2==2.7.3','MarkupSafe==0.23','Werkzeug==0.9.6',
				'bitcoin-python==0.3','commontools==0.1.0','itsdangerous==0.24',
				'pylibmc==1.3.0','requests==2.3.0'],
	zip_safe=False,
	keywords = ['python', 'bitcoin', 'namecoin', 'rpc'],
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
)
