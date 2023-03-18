#!/usr/bin/env python3
"""Authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _generate_uuid() -> str:
    """Generate and return 
       string type uuid
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Return hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """func to hash newly registered password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)    
        return new_user
    
    def valid_login(self, email: str, password: str) -> bool:
        """Verrify if the Login detail are correct
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_pwd)
        except (NoResultFound, InvalidRequestError):
            return False
        
    def create_session(self, email: str) -> str:
        """Genrate a session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user = self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user through the session_id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except:
            return None
        
    def destroy_session(self, user_id: int) -> None:
        """Updates user's session_id to None
        """
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            session_id = None
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        
    def get_reset_password_token(self, email: str) -> str:
        """Generate new token with uuid4
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except:
            raise ValueError

