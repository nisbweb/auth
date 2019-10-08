import pymongo
import os
import uuid
import hashlib
import datetime

client = pymongo.MongoClient(os.environ["MONGO"], connect=False)
db = client.auth


def verify_credential(email, password):
    ms = db.credentials.find_one({
        "email": email,
        "password": hashlib.sha256(password.encode()).hexdigest()
    })
    if ms:
        return True
    return False


def add_credential(email, password):
    credential = {
        "email": email,
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "timestamp": datetime.datetime.today()
    }
    db.credentials.insert_one(credential)


def update_credential(email, password):
    credential = {
        "email": email,
        "password": hashlib.sha256(password.encode()).hexdigest()
    }
    db.credentials.find_one_and_replace({"email": email}, credential)


def check_credentials_exist(email):
    if db.credentials.find_one({"email": email}):
        return True
    else:
        return False


def add_auth(email):
    token = uuid.uuid4().hex
    db.auths.insert_one({
        "email": email,
        "token": token,
        "timestamp": datetime.datetime.today()
    })
    return token


def get_auth(email):
    auths_list = []
    auths = db.auths.find({"email": email})
    if auths:
        for a in auths:
            auths_list.append(a["token"])
    return auths_list


def verify_auth(token):
    if db.auths.find_one({"token": token}):
        return True
    else:
        return False


def delete_all_auth(email):
    db.auths.delete_many({"email": email})


def delete_auth(token):
    db.auths.delete_one({"token": token})


# Password Reset
def save_reset_token(email, token):
    db.reset_tokens.insert_one({
        "email": email,
        "token": token,
        "timestamp": datetime.datetime.today()
    })


def get_reset_tokens(email):
    tokens_list = []
    tokens = db.reset_tokens.find({"email": email})
    if tokens:
        for token in tokens:
            tokens_list.append(token["token"])
    return tokens_list


def remove_reset_tokens(email):
    db.reset_tokens.delete_many({"email": email})
