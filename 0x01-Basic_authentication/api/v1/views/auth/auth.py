#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar


class Auth:
    """
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        """
        if path not in excluded_paths and path and excluded_paths:
            return True
        if excluded_paths == []:
            True
        if path + '/' == excluded_paths or path == excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authoriztion')
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        return None