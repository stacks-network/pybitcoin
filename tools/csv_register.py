#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import requests
import urllib
import json

url = 'http://127.0.0.1:5000/namecoind/name_new'

#-----------------------------------
def register_name(key, value):

    payload = {
                'key' : key,
                'value' : value,
            }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    resp = requests.post(url, data=payload, headers=headers)
    
    print resp.text
    
#-----------------------------------
if __name__ == '__main__':

    with open('data.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #register_name(row[0], row[1])
            print row