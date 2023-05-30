#!/usr/bin/env python3
"""
API basic authentication.
"""
from .auth import Auth


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
