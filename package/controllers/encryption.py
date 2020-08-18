#!/usr/bin/env python3

import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(input_str, mast_pass, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(mast_pass.encode('utf-8')))
    f = Fernet(key)

    return f.encrypt(input_str.encode('utf-8')).decode('utf-8')


def decrypt(input_str, mast_pass, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(mast_pass.encode('utf-8')))
    f = Fernet(key)

    return f.decrypt(input_str.encode('utf-8')).decode('utf-8')
