from datetime import datetime, timedelta, timezone
from typing import Union
from os import environ as env
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..model import schemas
from ..db import database
from . import repository
from ..tools.logging import logger

load_dotenv()

# Configurações do JWT
SECRET_KEY = env.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Contexto para hash de senha e Token
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
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.info(f"Creating access token with expiration: {expire.isoformat()}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"JWT created: {encoded_jwt}")
    return encoded_jwt

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    logger.info("Fetching current user from token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        exp: int = payload.get("exp")
        current_time = datetime.now(timezone.utc)
        logger.info(f"Token decoded, user_id: {user_id}, exp: {exp}, current_time: {current_time.isoformat()}")

        if user_id is None:
            logger.warning("User ID not found in token payload")
            raise credentials_exception

    except JWTError as e:
        logger.error(f"JWT Error decoding token: {e}")
        raise credentials_exception

    # Verifica se o token foi usado
    if repository.is_token_used(db, token):
        logger.warning("Token has already been used")
        raise HTTPException(status_code=401, detail="Token has already been used")

    # Busca o usuário pelo ID
    user = repository.get_customer(db, customer_id=user_id)
    if user is None:
        logger.warning(f"User not found with ID: {user_id}")
        raise credentials_exception

    # Marca o token como usado
    repository.mark_token_as_used(db, token)
    logger.info(f"User authenticated: {user.email}")

    # Retorna os dados do usuário
    return schemas.Customer(
        id=user_id,
        name=user.name,
        email=user.email,
        cpf=user.cpf
    )
