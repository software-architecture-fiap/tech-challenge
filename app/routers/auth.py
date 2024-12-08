from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..model import schemas
from ..services import repository, security
from ..tools.logging import logger

router = APIRouter()

@router.post('/token', tags=['auth'], response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica o Usuário e Gera um Token de Acesso.

    Este endpoint permite que um usuário obtenha um token de acesso
    fornecendo um nome de usuário e senha válidos.

    Args:
        db (Session, opcional): Instância de sessão do banco de dados.
        form_data (OAuth2PasswordRequestForm, opcional): Dados do formulário de login.

    Returns:
        dict: Um dicionário contendo o token de acesso e o ID do cliente.

    Raises:
        HTTPException: Se o nome de usuário ou a senha estiverem incorretos.
    """
    user = repository.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        logger.warning(f'Login falhou para o usuário: {form_data.username}')
        raise HTTPException(
            status_code=400,
            detail='Nome de usuário ou senha incorretos',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={'sub': str(user.id)}, expires_delta=access_token_expires)

    logger.info(f'Token criado para o ID do usuário: {user.id}')
    return {'access_token': f'{access_token}', 'customer_id': str(user.id)}
