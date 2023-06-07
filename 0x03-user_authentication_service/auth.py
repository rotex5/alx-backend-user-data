#!/usr/bin/env python3
"""Authentication Module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """returns bytes(i.e Slat hashed password passed in)"""
    encoded_pwd = password.encode('utf8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """returns a string represenation of Generated a uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user if they do not already exist
        """
        try:
            user_check = self._db.find_user_by(email=email)

        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, str(hashed_pwd))
            return user

        raise ValueError("Use {} already exists".format(user_check.email))

    def valid_login(self, email: str, password: str) -> bool:
        """Returns True or False based on Credential Validation
        """
        try:
            user_check = self._db.find_user_by(email=email)
            if user_check:
                encoded_pwd = password.encode('utf8')
                stored_hash = user_check.hashed_password
                return bcrypt.checkpw(encoded_pwd, stored_hash)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """return session id"""
        try:
            user_check = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user_check.id, session_id=session_id)
        return session_id
