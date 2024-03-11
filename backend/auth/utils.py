"""
Utility functions for authentication
"""
# import env variable tools
import os

# creating jwt
from datetime import timedelta, datetime
from jose import JWTError, jwt

# fast API tools
from fastapi import Depends
# import security modules
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# database connector
from database.connector.user import get_user_in_db_by_username, get_user_in_db_by_email

# user model
from .models import User, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Takes in the plain password and verifies that
    its is the same as the password stored in the system
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str, salt: str) -> str:
    """
    Get the hash of the password
    :param salt:
    :param password:
    :return:
    """
    return pwd_context.hash(password+salt)


def get_user_from_db(username: str):
    """
    Utility function to allow login with either email or username
    :param username:
    :return:
    """
    by_username = get_user_in_db_by_username(username)
    by_email = get_user_in_db_by_email(username)
    if by_username is not None:
        return by_username
    if by_email is not None:
        return by_email
    return None


def authenticate_user(username: str, password: str) -> User | None:
    """
    Takes in a username and password and returns a User Class
    :param username:
    :param password:
    :return:
    """
    user = get_user_from_db(username)

    if not user:
        return None

    if verify_password(password+user.salt, user.password):
        return User(username=user.username)

    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generates a JWT for the user
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("OAUTH_SECRET_KEY"),
                             algorithm=os.getenv("OAUTH_ALGORITHM"))
    return encoded_jwt


def get_user(username: str) -> UserResponse | None:
    """
    Gets username and returns the User Class
    :param username:
    :return: User class
    """
    user = get_user_from_db(username)

    if not user:
        return None

    return UserResponse(
        user_id=user.id,
        username = user.username,
        email=user.email,

        profile_picture=user.profile_picture,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday
            )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Gets current user from JWT and returns the user Class
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, os.getenv("OAUTH_SECRET_KEY"),
                             algorithms=[os.getenv("OAUTH_ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            return "Cannot get JWT from token"
    except JWTError:
        return "JWT Error"
    user = get_user(username=username)
    if user is None:
        return "User Does Not Exist"
    return user


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    """
    Gets current active user from token and returns the user Class
    :param current_user:
    :return:
    """
    return current_user
