#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import requests
import urllib
import json

url = 'http://127.0.0.1:5000/namecoind/name_update'

from pymongo import Connection

con = Connection()
db = con['namecoin']
queue = db.queue

#-----------------------------------
def utf8len(s):
    return len(s.encode('utf-8'))

#-----------------------------------
def do_nameupdate(key,new_value):

    reply = queue.find_one({'key':key})
    #new_value = json.loads(new_value)

    if reply == None: 
        print key + " not in DB"
        return 

    try: 
        temp = json.loads(reply['tx_id'])
        temp2 = temp['code']
        print "need name_firstupdate first"
    except:
        #name_firstupdate was successful 

        payload = {
                    'key' : key,
                    'new_value' : json.dumps(new_value),
                    }

        print key
        print payload['new_value']

        resp = requests.post(url, data=payload)
        print resp.text
        print '---'
        sleep(3)

#-----------------------------------
def format_key_value(key, value):

 
    if utf8len(str(value)) > 519:
        print "error: more than 519 bytes in value"
        raise RuntimeError
    
    return key, value

#-----------------------------------
def main_loop(key, value):

    key, value = format_key_value(key,value)

    do_nameupdate(key, value)

#-----------------------------------
if __name__ == '__main__':

    key = "u/ryan"

    from pymongo import Connection
    con = Connection()
    db = con['namecoin']
    queue = db.queue

    reply = queue.find_one({'key':key})

    #data = reply['value']

    json_data=open('json_profile.json')
    data = json.load(json_data)

    #reply['value'] = data 
    #queue.save(reply)

    #print reply 

    main_loop(key, data)