"""
Models for authentication
"""
from typing import Optional
from datetime import date

from pydantic import BaseModel


class User(BaseModel):
    """
    User model for FastAPI application
    """
    username: str


class UserResponse(BaseModel):
    """
    Mirror of UserDB for use with fast api endpoints
    """
    user_id: int
    username: str
    email: str

    profile_picture: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]


class Token(BaseModel):
    """
    Model to store
    :param username:
    :param token_type:
    """
    access_token: str
    token_type: str


class LoginCredentials(BaseModel):
    """
    Model to accept login credentials
    :param username:
    :param password:
    """
    username: str
    password: str
