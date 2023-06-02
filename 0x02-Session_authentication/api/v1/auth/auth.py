#!/usr/bin/env python3
"""
API authentication.
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """
    class representation of an API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """True if path is not in excluded_paths, else False"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        else:
            for excluded_path in excluded_paths:
                if excluded_path.startswith(path):
                    return False
                if excluded_path.endswith(path):
                    return False
                if excluded_path[-1] == "*":
                    if path.startswith(excluded_path[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """return authorization header from a request object
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns currently authorized user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        session_id = request.cookies.get(SESSION_NAME)
        return session_id
