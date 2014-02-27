#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import csv
import requests
import json

import random
import string

url = 'http://127.0.0.1:5000/namecoind/name_new'

from pymongo import Connection
con = Connection()
db = con['namecoin']
queue = db.queue

#-----------------------------------
def get_random_string(size=10):
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(size)]
    return "".join(lst)

#-----------------------------------
def utf8len(s):
    return len(s.encode('utf-8'))

#-----------------------------------
def slice_profile(username, profile):

    #need u/ for OneName usernames
    key1 = 'u/' + username.lower()
    key2 = 'i/' + username.lower() + '-1'

    value1 = {}
    value2 = {}

    first_keys = ['v', 'name', 'bitcoin', 'pgp', 'website', 'location', 'bio']

    for key in profile.keys():
        if(key in first_keys):
            value1[key] = profile[key]
        else:
            value2[key] = profile[key]
            
    #don't allow more than 519 bytes of data in the namecoin blockchain (their bug/limit)
    if utf8len(str(value1)) > 519 or utf8len(str(value2)) > 519:
        print "error: more than 519 bytes in value"
        raise RuntimeError

    if value2.keys() == []:
        return key1, value1, None, None 
    else:
        value1['next'] = key2
        return key1, value1, key2, value2 

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
def main_loop(username,profile):

    key1, value1, key2, value2 = slice_profile(username,profile)

    reply = queue.find_one({'key':key1})

    try:
        temp = reply['key1']
    except:
        #not in DB 
        print "not registered: " + key1
        register_name(key1,value1)
        if key2 is not None:
            register_name(key2,value2)

#-----------------------------------
if __name__ == '__main__':

    '''
    with open('data.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            main_loop(row[0], row[1])
    '''

    from pymongo import MongoClient

    MONGODB_URI = 'mongodb://heroku_app22080231:vphfu4445c5f72636n3mmvotpt@ds033699.mongolab.com:33699/heroku_app22080231'
    remote_client = MongoClient(MONGODB_URI)
    users = remote_client['heroku_app22080231'].user

    for i in users.find():
        if i['registered'] is False:
            main_loop(i['username'],json.loads(i['profile']))
