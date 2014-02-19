
#----------------------------------------------
###Copying some functions from coinsrpc.py as these functions are giving a context error if imported here;
###There should probably be a better approach for this. For now, going with copying functions
    
def namecoind_blocks():

    reply = {}
    info = namecoind.getinfo()
    reply['blocks'] = info.blocks
    return json.dumps(reply)

#----------------------------------------------
def namecoind_firstupdate(name, rand, value):

    info = namecoind.name_firstupdate(name, rand, value)
    return json.dumps(info)

#----------------------------------------------
def unlock_wallet(passphrase, timeout=10):
    
    info = namecoind.walletpassphrase(passphrase, timeout, True)
    return info             #info will be True or False

#----------------------------------------------
def register_name(name):
    return namecoind.name_new(name)         #returns a list of [longhex, rand]
    
#----------------------------------------------

#When this script is run, it will check Mongodb and find domains which aren't
#registered yet. This will then register domains for which 12 blocks have been
#passed. Finally the script will mark the domain status as registered.

import json
from time import sleep
from pymongo import Connection
import bitcoinrpc 
#from coinsrpc_api import namecoind_blocks, namecoind_firstupdate, unlock_wallet
from config import * 

namecoind = bitcoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, 
					host=NAMECOIND_SERVER, port=NAMECOIND_PORT, use_https=NAMECOIND_USE_HTTPS)

con = Connection()
db = con['namecoin']
domains = db.domains

domains_collection = domains.find()

passphrase = input('Please enter wallet passphrase (in quotes)\n')

while True:
    print "Starting running the script"
    
    for domain in domains_collection:
        if domain.get('registered') is not None and domain.get('registered') == False :

            #register domain here

            reg_type = domain.get('reg_type')
            if reg_type == 'domain':
                name = 'd/' + domain.get('name')
            elif reg_type == 'username':
                name = 'u/' + domain.get('name')
            else:
                name = domain.get('name')           #advanced case

            print "Registering name %s" % name
            
            #first unlock the wallet
            if not unlock_wallet(passphrase):
                print "passphrase is incorrect\n"
                break
                
            info = register_name(name)

            domain['longhex'] = info[0]
            domain['rand'] = info[1]                   
            domain['registered'] = True

            block_info = json.loads(namecoind_blocks())
            domain['current_block'] = block_info['blocks']
            domain['wait_till_block'] = block_info['blocks']+ 12
            domain['activated'] = False
            
            domains.save(domain)
                                 
                                
        elif domain.get('activated') is not None and domain.get('activated') == False:   #domain is registered; but not activated
            
            #compare the current block with 'wait_till_block'
            block_info = json.loads(namecoind_blocks())

            if block_info['blocks'] > domain['wait_till_block']:
                #lets activate the domain

                print "Activating domain: %s to point to %s" % (domain['name'], domain['value'])
                
                #first unlock the wallet
                if not unlock_wallet(passphrase):
                    print "passphrase is incorrect\n"
                    break
                    
                

                if domain.get('type') is not None and domain.get('type') == 'advanced':
                    update_value = domain['value']      #its already a json value...
                else:
                    update_value = json.dumps({"map":{"": domain['value']}})
                    
                output = namecoind_firstupdate(domain['name'], domain['rand'], update_value)
                print "Transaction ID ", output

                domain['activated'] = True
                domain['tx_id'] = output
                domains.save(domain)
           

    print "Sleeping for a while"
    sleep(60 * 10)
    
