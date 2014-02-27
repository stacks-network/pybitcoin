#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import csv
import requests
import urllib
import json

url = 'http://127.0.0.1:5000/namecoind/name_new'

from pymongo import Connection
con = Connection()
db = con['namecoin']
queue = db.queue

#-----------------------------------
def format_key_value(key, name=None):

    #need u/ for OneName usernames
    key = 'u/' + key.lower()

    value = {}

    value['status'] = "reserved"

    if name is not None and name != '': 

        value["message"] = "This OneName username is reserved for " + name.lstrip(' ') 
        value["message"] += ". If this is you, please email reservations@onename.io to claim it for free."

    else:

        value["message"] = "This OneName username was parked to evade name squatting, but can be made available upon reasonable request"
        value["message"] += " at no charge. If you are interested in this name, please email reservations@onename.io with your twitter"
        value["message"] += " handle and why you would like this particular name."

    return key, value 

#-----------------------------------
def register_name(key, value):

    payload = {
                'key' : key,
                'value' : json.dumps(value),
            }

    print key
    print payload['value']

    resp = requests.post(url, data=payload)
    print resp.text
    print '---'
    sleep(3)

#-----------------------------------
def main_loop(key, name=None):

    key, value = format_key_value(key,name)

    reply = queue.find_one({'key':key})

    try:
        temp = reply['key']
    except:
        #not in DB 
        print "not registered: " + key
        #register_name(key,value)

#-----------------------------------
if __name__ == '__main__':

    with open('data.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            main_loop(row[0], row[1])

