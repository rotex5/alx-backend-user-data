#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string. """
    encoded_pass = password.encode()
    hashed_pass = bcrypt.hashpw(encoded_pass, bcrypt.gensalt())
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Returns True if password is value, else False"""
    encoded_pass = password.encode()
    if bcrypt.checkpw(encoded_pass, hashed_password):
        return True
    else:
        return False
