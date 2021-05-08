# -*- coding: utf-8 -*-
import base64
import hashlib
from config import PASS_KEY, TOKEN_KEY


def encryption(str):
    hash = hashlib.md5(PASS_KEY)
    hash.update(str.encode('utf-8'))
    return hash.hexdigest()


def get_token(payload):
    # first = base64.b64encode(aes_encrypt(payload,AES_KEY))
    first = base64.b64encode(payload)
    sha = hashlib.sha256(TOKEN_KEY)
    sha.update(first)
    second = sha.hexdigest()
    token = first + '.' + second
    return token
