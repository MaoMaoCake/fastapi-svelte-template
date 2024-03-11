"""
Authentication Routes
"""
import os
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException

from .models import LoginCredentials, Token, UserResponse
from .utils import create_access_token, get_current_active_user, authenticate_user

authRouter = APIRouter()

@authRouter.post("/token", tags=["Auth"])
async def login_for_access_token(login_credential: LoginCredentials) -> Token:
    """
    Takes Username and password and signs a token
    :param login_credential:
    :return:
    """
    user = authenticate_user(login_credential.username, login_credential.password)
    if not user:
        raise HTTPException(404, detail="Username or password incorrect")

    access_token_expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@authRouter.get("/user/me", tags=["Auth"])
async def get_user_info(current_user: UserResponse = Depends(get_current_active_user))\
        -> UserResponse | None:
    """
    Returns user information
    :param current_user:
    :return:
    """
    return current_user
