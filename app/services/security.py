from datetime import datetime, timedelta
from typing import Union
from os import environ as env
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..model import models, schemas

from ..db import database
from . import repository
from ..tools.logging import logger

load_dotenv()

# Configurações do JWT
SECRET_KEY = env.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    logger.debug(f"Verifying password for user")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    logger.debug(f"Hashing password")
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = repository.get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if repository.is_token_used(db, token):
        raise HTTPException(status_code=401, detail="Token has already been used")

    user = repository.get_user_by_email(db, email=username)
    if user is None:
        raise credentials_exception
    
    # Mark the token as used after it's validated
    repository.mark_token_as_used(db, token)

    return user
