from datetime import datetime, timedelta, timezone
from os import environ as env
from typing import Union, Optional
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..db import database
from ..model import schemas, models
from ..tools.logging import logger
from ..db.database import get_db

load_dotenv()

# Configurações do JWT
SECRET_KEY = env.get('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 5

# Contexto para hash de senha e Token
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde à senha criptografada.

    Args:
        plain_password (str): Senha fornecida pelo usuário.
        hashed_password (str): Senha criptografada armazenada.

    Returns:
        bool: True se a senha corresponder, False caso contrário.
    """
    logger.debug('Verifying password for user')
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash para a senha fornecida.

    Args:
        password (str): Senha a ser criptografada.

    Returns:
        str: Senha criptografada.
    """
    logger.debug('Hashing password')
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Union[schemas.Customer, bool]:
    """Autentica um usuário com base no nome de usuário e senha fornecidos.

    Args:
        db (Session): Sessão do banco de dados.
        username (str): Nome de usuário ou e-mail.
        password (str): Senha fornecida pelo usuário.

    Returns:
        Union[schemas.User, bool]: O usuário autenticado ou False se a autenticação falhar.
    """
    from .repository import get_user_by_email 
    user = get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """Cria um token JWT com base nos dados fornecidos e tempo de expiração.

    Args:
        data (dict): Dados a serem incluídos no token.
        expires_delta (Union[timedelta, None], optional): Tempo adicional para expiração do token. Defaults to None.

    Returns:
        str: Token JWT gerado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    logger.info(f'Creating access token with expiration: {expire.isoformat()}')
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f'JWT created: {encoded_jwt}')
    return encoded_jwt

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> schemas.Customer:
    """Obtém o usuário atual com base no token JWT fornecido.

    Args:
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(database.get_db).
        token (str, optional): Token JWT fornecido. Defaults to Depends(oauth2_scheme).

    Returns:
        schemas.Customer: Dados do usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido, expirado ou o usuário não for encontrado.
    """
    logger.info('Fetching current user from token')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('sub')
        exp: int = payload.get('exp')
        current_time = datetime.now(timezone.utc)
        logger.info(f'Token decoded, user_id: {user_id}, exp: {exp}, current_time: {current_time.isoformat()}')

        if user_id is None:
            logger.warning('User ID not found in token payload')
            raise credentials_exception

    except JWTError as e:
        logger.error(f'JWT Error decoding token: {e}')
        raise credentials_exception

    # Verifica se o token foi usado
    from .repository import is_token_used
    if is_token_used(db, token):
        logger.warning('Token has already been used')
        raise HTTPException(status_code=401, detail='Token has already been used')

    # Busca o usuário pelo ID
    from .repository import get_customer
    user = get_customer(db, customer_id=user_id)
    if user is None:
        logger.warning(f'User not found with ID: {user_id}')
        raise credentials_exception

    # Marca o token como usado
    from .repository import mark_token_as_used
    mark_token_as_used(db, token)
    logger.info(f'User authenticated: {user.email}')

    # Retorna os dados do usuário
    return schemas.Customer(id=user_id, name=user.name, email=user.email, cpf=user.cpf)

def get_optional_user(db: Session = Depends(get_db), user_id: Optional[int] = None) -> Optional[models.Customer]:
    """
    Retorna o cliente autenticado com base no token, ou None se o token for inválido ou ausente.
    """
    try:
        if not user_id:
            return None

        customer = db.query(models.Customer).filter(models.Customer.id == user_id).first()
        return customer
    except Exception as e:
        logger.error(f"Erro ao obter cliente opcional: {e}", exc_info=True)
        return None
