from html2text import html2text
import requests
import json
from flask import jsonify, Blueprint, request
from coinrpc.namecoind_api import error_reply
from coinrpc.coinrpc import get_full_profile

checker_api = Blueprint('checker_api', __name__)

#-----------------------------------------
def is_valid_proof(key, value, username):

    proof_url = get_proof_url(value["proof"], username)
    if "username" in value:
        site_username = value["username"]
        if site_username not in proof_url:
            return False
    r = requests.get(proof_url)
    search_text = html2text(r.text)
    if key == "twitter":
        search_text = search_text.replace("<s>", "").replace("</s>", "").replace("**", "")
    elif key == "github":
        pass
    elif key == "facebook":
        pass
    search_text = search_text.lower()
    if "verifymyonename" in search_text and ("+" + username) in search_text:
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

    username = request.args.get('username')

    if username is None:
        return error_reply("username not given")

    profile = get_full_profile('u/' + username)

    proof_sites = ["twitter", "github", "facebook"]

    for key, value in profile.items():
        if key in proof_sites and type(value) is dict and "proof" in value:
            if is_valid_proof(key, value, username):
                verifications[key] = True
    
    return jsonify(verifications)