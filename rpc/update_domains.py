#When this script is run, it will check Mongodb and find domains which aren't
#registered yet. This will then register domains for which 12 blocks have been
#passed. Finally the script will mark the domain status as registered.

from pymongo import Connection
from coinsrpc_api import namecoind_blocks, namecoind_firstupdate, unlock_wallet
import json
from time import sleep

con = Connection()
db = con['namecoin']
domains = db.domains

domains_collection = domains.find()

#wallet_passphrase = input('Please enter wallet passphrase (in quotes)\n')

while True:
    print "Starting running the script"
    
    for domain in domains_collection:
        if not domain['activated']:
            #compare the current block with 'wait_till_block'
            block_info = json.loads(namecoind_blocks())

            if block_info['blocks'] > domain['wait_till_block']:
                #lets activate the domain

                #first unlock the wallet
                #unlock_wallet(passphrase)
                #print "passphrase is incorrect\n"
                #break
                
                print "Activating domain: %s to point to %s" % (domain['name'], domain['value'])
                
                update_value = json.dumps({"map":{"": domain['value']}})
                output = namecoind_firstupdate(domain['name'], domain['rand'], update_value)
                print "Transaction ID ", output

                domain['activated'] = True
                domain['tx_id'] = output
                domains.save(domain)
           

    print "Sleeping for a while"
    sleep(60 * 10)             
