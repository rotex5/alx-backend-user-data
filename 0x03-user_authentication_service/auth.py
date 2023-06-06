#!/usr/bin/env python3
"""Authentication Module
"""
import bcrypt
from typing import ByteString


def _hash_password(password: str) -> bytes:
    """returns bytes(i.e Slat hashed password passed in)"""
    encoded_pwd = password.encode()
    hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
    return hashed_pwd
