#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep
from pymongo import Connection
from coinrpc.coinrpc import namecoind_blocks, namecoind_firstupdate, unlock_wallet
from config import entered_passphrase

con = Connection()
db = con['namecoin']
queue = db.queue

collection = queue.find()

#-----------------------------------
if __name__ == '__main__':

    print "Starting script"
    
    for entry in collection:

        if entry.get('activated') is not None and entry.get('activated') == False:   #entry is registered; but not activated
            
            #compare the current block with 'wait_till_block'
            #block_info = json.loads(namecoind_blocks())
            block_info = namecoind_blocks()

            if block_info['blocks'] > entry['wait_till_block']:
                #lets activate the entry

               #check if 'value' is a json or not
                try:
                    update_value = json.loads(entry['value'])
                    update_value = json.dumps(update_value)     #no error while parsing; dump into json again
                except ValueError:
                    update_value = entry['value']    #error: treat it as a string

                print "Activating entry: '%s' to point to '%s'" % (entry['key'], update_value)
                
                #first unlock the wallet
                if not unlock_wallet(entered_passphrase):
                    print "passphrase is incorrect\n"
                    break
                    
                output = namecoind_firstupdate(entry['key'], entry['rand'], update_value, entry['longhex'])
                print "Transaction ID ", output

                entry['activated'] = True
                entry['tx_id'] = output
                queue.save(entry)

    '''
    print "Sleeping for a while"
    sleep(60 * 10)
    '''
    print "Finished script"
