#!/usr/bin/env python3
"""
API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    class representation of an API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """True if path is not in excluded_paths, else False"""
        return False

    def authorization_header(self, request=None) -> str:
        """return authorization header from a request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns currently authorized user"""
        return None
