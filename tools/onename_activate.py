#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

from time import sleep

SERVER_URL = 'http://127.0.0.1:5000/namecoind/'

resp = requests.get(SERVER_URL + 'blocks')
namecoind_blocks = resp.json()

from pymongo import Connection
con = Connection()
db = con['namecoin']
queue = db.queue

#-----------------------------------
def check_name_firstupdate_errors(key):

    reply = queue.find_one({'key':key})

    try:
        if(reply['activated'] is True):
        
            try: 
                temp = json.loads(reply['tx_id'])
                print temp['code']
                print key + " had error"
                reply['activated'] = False
                queue.save(reply)
            except:
                pass
    except Exception as e:
        print key + " not in DB"

#-----------------------------------
if __name__ == '__main__':

    print "Starting script"
    print '---'

    #first check for errors of last run and set activated = False
    #for entry in queue.find():
    #    check_name_firstupdate_errors(entry['key'])
    
    for entry in queue.find():

        if entry.get('activated') is not None and entry.get('activated') == False:   #entry is registered; but not activated
            
            #print entry
            print "Processing: " + entry['key'] 

            #compare the current block with 'wait_till_block'
            current_blocks = namecoind_blocks['blocks']

            if current_blocks > entry['wait_till_block']:
                #lets activate the entry

               #check if 'value' is a json or not
                try:
                    update_value = json.loads(entry['value'])
                    update_value = json.dumps(update_value)     #no error while parsing; dump into json again
                except ValueError:
                    update_value = entry['value']    #error: treat it as a string

                print "Activating entry: '%s' to point to '%s'" % (entry['key'], update_value)
            
                payload = {}
                payload['key'] = entry['key']
                payload['rand'] = entry['rand']
                payload['value'] = update_value
                payload['tx'] = entry['longhex']

                resp = requests.post(SERVER_URL + 'name_firstupdate', data=payload)
                output = resp.json()

                #output = namecoind_firstupdate(entry['key'], entry['rand'], update_value, entry['longhex'])
                print "Transaction ID ", output

                if 'code' in output:
                    entry['activated'] = False
                else:
                    entry['activated'] = True

                entry['tx_id'] = output
                queue.save(entry)

                sleep(3)
            else:
                print "Wait for %s more blocks" % (entry['wait_till_block'] - current_blocks)

            print '----'

    print "Finished script"