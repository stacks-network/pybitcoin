#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

import requests
import json  

#-------------------------
def test_api(server):
	
	url = 'https://localhost:5000/namecoind/fg_scan'

	if(server == 'remote'):
		url = 'https://ocean2.halfmoonlabs.com/namecoind/fg_scan'
	
	print url 

	data = {}
	data['username'] = 'd/ryanshea'
	
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Basic'}

	r = requests.get(url, data=json.dumps(data), headers=headers, auth=('coinrpc','password'))

	pretty_print(r.json())

	print '-' * 10

#-------------------------    
if __name__ == "__main__":

	server = 'local'		

	try:
		server = sys.argv[1]
	except:
		pass

	test_api(server)