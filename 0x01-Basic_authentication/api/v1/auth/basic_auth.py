#!/usr/bin/env python3
"""
API basic authentication.
"""
from .auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    class representation of an BasicAuth.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a
        Base64 string base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            utf8_encode = base64_authorization_header.encode("utf-8")
            decode64 = b64decode(utf8_encode)
            return decode64.decode("utf-8")

        except BaseException:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ returns the user email and password from
        the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        value = decoded_base64_authorization_header.split(":", 1)
        value_1 = value[0]
        value_2 = value[1]
        return (value_1, value_2)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users_search = User.search({"email": user_email})
        except Exception:
            return None

        for user in users_search:
            if not user.is_valid_password(user_pwd):
                return None
            else:
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a reques"""
        author_header = self.authorization_header(request)

        if not author_header:
            return None

        encoded = self.extract_base64_authorization_header(author_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, password = self.extract_user_credentials(decoded)

        if not email or not password:
            return None

        current_user = self.user_object_from_credentials(email, password)

        return current_user
