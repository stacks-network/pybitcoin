#!/usr/bin/env python
#-----------------------
# Copyright 2014 Halfmoon Labs, Inc.
# All Rights Reserved
#-----------------------

'''
	For testing the API from command line 
'''

import requests
import json  

REMOTE_SERVER = 'http://coinrpc.halfmoonlabs.com'
API_ENDPOINT = '/bitcoind/getinfo'

#-------------------------
def call_api(address,auth_user,auth_passwd,server='local'):
	
	url = 'http://localhost:5000' + API_ENDPOINT

	if(server == 'remote'):
		url = REMOTE_SERVER + API_ENDPOINT

	data = {}
	data['address'] = address

	print url 
	print data 

	headers = {'Content-type': 'application/json'}

	r = requests.get(url, params=data, headers=headers, auth=(auth_user,auth_passwd))

	if r.status_code == 401:
		print "Wrong user/passwd"
	else:
		print r.json()
		print '-' * 10

#-------------------------    
if __name__ == "__main__":

	import sys 
	try:
		address = sys.argv[1]
		auth_user = sys.argv[2]
		auth_passwd = sys.argv[3]
	except:
		print "ERROR: need <address>, <auth_user>, <auth_passwd>"
		exit()

	call_api(address, auth_user, auth_passwd)