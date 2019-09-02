import pymongo
import os
import uuid
import hashlib

client = pymongo.MongoClient(os.environ["MONGO"],connect=False)
db = client.auth

def verify_credential(email,password):
    ms = db.credentials.find_one({"email":email,"password":hashlib.sha256(password.encode())})
    if ms:
        return True
    return False

def add_credential(email,password):
    credential = {
        "email":email,
        "password":hashlib.sha256(password.encode())
    }
    db.credentials.insert_one(credential)

def update_credential(email,password):
    credential = {
        "email":email,
        "password":hashlib.sha256(password.encode())
    }
    db.credentials.find_one_and_replace({"email":email},credential)



def add_auth(email):
    token = uuid.uuid4().hex
    db.auths.insert_one({
        "email":email,
        "token":token
    })
    return token

def get_auth(email):
    auths_list=[]
    auths = db.auths.find({"email":email})
    if auths:
        for a in auths:
            auths_list.append(a["token"])
    return auths_list

def verify_auth(token):
    if db.auths.find_one({"token":token}):
        return True
    else:
        return False
    

def delete_all_auth(email):
    db.auths.delete({"email":email})

def delete_auth(token):
    db.auths.delete_one({"token":token})

