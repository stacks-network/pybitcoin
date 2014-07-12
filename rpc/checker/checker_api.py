from html2text import html2text
import requests
import json
from flask import jsonify, Blueprint, request
from namecoin.namecoind_api import error_reply
from namecoin.namecoind_wrapper import get_full_profile

from config import MEMCACHED_ENABLED, MEMCACHED_PORT, MEMCACHED_TIMEOUT, DEFAULT_HOST
from config import MONGODB_URI

import pylibmc
from time import time
mc = pylibmc.Client([DEFAULT_HOST + ':' + MEMCACHED_PORT],binary=True)

checker_api = Blueprint('checker_api', __name__)

import hashlib 

#-----------------------------------
from pymongo import MongoClient

remote_client = MongoClient(MONGODB_URI)
remote_db = remote_client.get_default_database()
users = remote_db.user

#-----------------------------------------
def get_json(data):

    if isinstance(data,dict):
        pass 
    else:
        data = json.loads(data)
        
    return data

#-----------------------------------------
def is_valid_proof(key, value, username, proof_url):

    #check if username is actually on that service (and not some other user)
    if "username" in value:
        site_username = value["username"].lower()
        if site_username not in proof_url.lower():
            return False

        if key == "twitter" and "twitter.com" not in proof_url:
            return False
        elif key == "github" and "github.com" not in proof_url:
            return False

    try:
        r = requests.get(proof_url)
    except:
        return False

    search_text = html2text(r.text)
    if key == "twitter":    
        search_text = search_text.replace("<s>", "").replace("</s>", "").replace("**", "")
    elif key == "github":
        pass
    
    search_text = search_text.lower()

    if "verifymyonename" in search_text and ("+" + username) in search_text:
        return True
    elif "verifying myself" in search_text and "bitcoin username" in search_text and ("+" + username) in search_text:
        return True
    elif "verifying myself" in search_text and "bitcoin username" in search_text and username in search_text:
        return True
 
    return False

#-----------------------------------------
def get_proof_url(proof, username):

    proof_url = None
    if "url" in proof:
        proof_url = proof["url"]
    elif "id" in proof:
        if key == "twitter":
            proof_url = "https://twitter.com/" + username + "/status/" + proof["id"]
        elif key == "github":
            proof_url = "https://gist.github.com/" + username + "/" + proof["id"]
        elif key == "facebook":
            proof_url = "https://www.facebook.com/" + username + "/posts/" + proof["id"]
    return proof_url

#-----------------------------------------
@checker_api.route('/checker/get_verifications')
def get_verifications():

    verifications = {}
    proof_sites = ["twitter", "github", "facebook"]

    username = request.args.get('username')

    try:
        refresh = int(request.args.get('refresh'))
    except:
        refresh = 0 

    if refresh == 1:
        USE_CACHE = False
    else:
        USE_CACHE = MEMCACHED_ENABLED

    if username is None:
        return error_reply("username not given")

    try: 
        user = users.find_one({"username":username})
        profile = get_json(user["profile"])

    except Exception as e:
        profile = get_full_profile('u/' + username)

    for key, value in profile.items():

        if key in proof_sites and type(value) is dict and "proof" in value:
            
            try:
                proof_username = value['username'].lower()
                proof_url = get_proof_url(value["proof"], proof_username)
                proof_url_hash = hashlib.md5(proof_url).hexdigest()

            except Exception as e:
                continue 

            if USE_CACHE: 
                cache_reply = mc.get("proof_" + proof_url_hash)
            else:
                cache_reply = None 
                #print "cache off"

            if cache_reply is None: 
              
                if is_valid_proof(key, value, username, proof_url):

                    verifications[key] = True
    
                    if USE_CACHE:
                        mc.set("proof_" + proof_url_hash,username,int(time() + MEMCACHED_TIMEOUT))
                        #print "cache miss"
            else:
                #print "cache hit"
                if cache_reply == username:
                    verifications[key] = True

    return jsonify(verifications)