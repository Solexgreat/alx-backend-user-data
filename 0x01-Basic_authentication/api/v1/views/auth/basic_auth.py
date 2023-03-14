#!/usr/bin/env python3
from api.v1.views.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the Basic value
        """
        if authorization_header and isinstance(
                authorization_header, 
                str) and authorization_header.startswith('Basic '):
            return authorization_header[6:]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string
        """
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                decoded = base64.b64decode(base64_authorization_header)
                return decoded.decode('utf-8')
            except:
                return None
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract the username and password 
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return (email, pwd)
    
    def user_object_from_credentials(self, user_email: str,
                                      user_pwd: str) -> TypeVar('User'):
        """Comfirm and Return the User 
        """
        if not isinstance(user_email, str) or not isinstance(
                user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users: 
            if user.is_valid_password(user_pwd):
                return user
    def current_user(self, request=None) -> TypeVar('User'):
        """Overrides Auth and retrieves User instance for request
        """
        headValue = Auth.authorization_header(request)
        BasicValue = self.extract_base64_authorization_header(headValue)
        decodedValue = self.decode_base64_authorization_header(BasicValue)
        email, pwd = self.extract_user_credentials(decodedValue)
        user = self.user_object_from_credentials(email, pwd)
        return user
