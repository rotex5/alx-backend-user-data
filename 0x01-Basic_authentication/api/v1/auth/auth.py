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
