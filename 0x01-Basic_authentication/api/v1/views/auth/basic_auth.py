#!/usr/bin/env python3
from api.v1.views.auth.auth import Auth
import base64


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
    
