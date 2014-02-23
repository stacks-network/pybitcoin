import json
import bitcoinrpc 
from pymongo import Connection
from config import *
from domain_validity import is_domain_valid
from helpers import conv_dict_to_list


namecoind = bitcoinrpc.connect_to_remote(NAMECOIND_USER, NAMECOIND_PASSWD, 
									host=NAMECOIND_SERVER, port=NAMECOIND_PORT, use_https=NAMECOIND_USE_HTTPS)

con = Connection()
db = con['namecoin']
filtered = db.filtered

max_returned = 5000
total_scanned = 0
valid_domains = 0;

# test for valid domain.
# a) starts with d/  b) match RegEx for a valid domain or IP...


print "Scanning first %d domains; total scanned = %d; valid domains found = %d" % (max_returned, total_scanned, valid_domains)
domains = namecoind.name_scan('!', max_returned)


while True:
    for domain in domains:

        #check if domain starts with d/
        if not domain.get('name').startswith('d/'):
            continue

        #check if the value is json-encoded or simply a string
        try:
            d = json.loads(domain.get('value'))
        except:
            d = domain.get('value')

        #find all the keys inside d  
        values = []
        conv_dict_to_list(d, values)
        
        #check if any of the values is valid
        for value in values:
            if is_domain_valid(value):
                print domain.get('name'), d
                valid_domains += 1

                #add to Mongo
                filtered.insert(domain)

                break
        

    total_scanned += len(domains)

    
    #domain['name'] now points to the last name that we scanned, so next time start from here...
    print "\nScanning next %d domains; total scanned = %d; valid domains found = %d" % (max_returned, total_scanned, valid_domains)
    
    try:
        domains = namecoind.name_scan(domain['name'], max_returned)
    except:
        pass
    
    #test for exit
    if len(domains) < 2:
        break
