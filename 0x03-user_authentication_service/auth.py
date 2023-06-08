#!/usr/bin/env python3
"""Authentication Module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """returns bytes(i.e Slat hashed password passed in)"""
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"),
                               bcrypt.gensalt())
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
                return bcrypt.checkpw(password.encode("utf-8"),
                                      user_check.hashed_password)
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

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """returns the corresponding User or None
        """
        if session_id is None:
            return None

        try:
            user_check = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user_check

    def destroy_session(self, user_id: int) -> None:
        """destroys existing session and updates the
        corresponding user’s session ID"""
        try:
            user_check = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user_check.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset token for identified user"""
        try:
            user_check = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user_check.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Upate user's password"""
        if reset_token is None or password is None:
            raise ValueError

        try:
            user_check = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user_check.id, hashed_password=hashed_password,
                             reset_token=None)
