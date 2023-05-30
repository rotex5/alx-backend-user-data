#!/usr/bin/env python3
"""
API basic authentication.
"""
from .auth import Auth
from base64 import b64decode


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
