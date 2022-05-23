#!/usr/bin/env python3
"""
Module auth
"""
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of
    the input password
    """
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    return hashed_password


def _generate_uuid() -> str:
    """
    Returns string representation
    of a new UUID
    """
    uid = str(uuid4())
    return uid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                    )
        except NoResultFound:
            return False
