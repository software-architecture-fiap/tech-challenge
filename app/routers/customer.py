from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..model import schemas
from ..services import repository
from ..tools.logging import logger

router = APIRouter()

@router.get('/', response_model=List[schemas.Customer])
def read_customers_or_customer(
    customer_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> Union[List[schemas.Customer], schemas.Customer]:
    """
    Recupera um cliente pelo ID ou uma lista de clientes com paginação.

    Args:
        customer_id (Optional[str]): O ID do cliente para recuperar.
        skip (int): O número de registros a serem ignorados (usado para paginação).
        limit (int): O número máximo de registros a serem retornados (usado para paginação).
        db (Session): A sessão do banco de dados.

    Raises:
        HTTPException: Se o formato do ID do cliente for inválido ou se o cliente não for encontrado.

    Returns:
        Union[List[schemas.Customer], schemas.Customer]: Os dados do cliente ou uma lista de clientes.
    """
    if customer_id:
        logger.info(f'Buscando cliente com ID: {customer_id}')
        try:
            customer_id_int = customer_id
        except (ValueError, IndexError):
            logger.warning(f'Formato inválido de ID de cliente: {customer_id}')
            raise HTTPException(status_code=400, detail='Formato de ID de cliente inválido')

        db_customer = repository.get_customer(db, customer_id=customer_id_int)
        if db_customer is None:
            logger.warning(f'Cliente com ID {customer_id} não encontrado')
            raise HTTPException(status_code=404, detail='Cliente não encontrado')
        return db_customer

    logger.info(f'Buscando clientes com skip: {skip}, limit: {limit}')
    customers = repository.get_customers(db, skip=skip, limit=limit)
    return customers

@router.post('/admin', response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)) -> schemas.Customer:
    """Cria um novo cliente com as informações fornecidas.

    Args:
        customer (schemas.CustomerCreate): Os dados do cliente para criar.
        db (Session): A sessão do banco de dados.

    Raises:
        HTTPException: Se um cliente com o e-mail fornecido já existir.

    Returns:
        schemas.Customer: O cliente criado.
    """
    logger.info(f'Criando cliente com o e-mail: {customer.email}')
    db_customer = repository.get_user_by_email(db, email=customer.email)
    if db_customer:
        logger.warning(f'Cliente com o e-mail {customer.email} já existe')
        raise HTTPException(status_code=400, detail='E-mail já registrado')
    created_customer = repository.create_user(db=db, user=customer)
    logger.info(f'Cliente criado com ID: {created_customer.id}')
    return created_customer

@router.post('/register', response_model=schemas.Customer)
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)) -> schemas.Customer:
    """Registra um novo cliente com as informações fornecidas.

    Args:
        customer (schemas.CustomerCreate): Os dados do cliente para registrar.
        db (Session): A sessão do banco de dados.

    Raises:
        HTTPException: Se um cliente com o e-mail fornecido já existir.

    Returns:
        schemas.Customer: O cliente registrado.
    """
    logger.info(f'Registrando cliente com e-mail: {customer.email}')
    db_customer = repository.get_user_by_email(db, email=customer.email)
    if db_customer:
        logger.warning(f'Cliente com o e-mail {customer.email} já existe')
        raise HTTPException(status_code=400, detail='E-mail já registrado')
    created_customer = repository.create_user(db=db, user=customer)
    logger.info(f'Cliente registrado com ID: {created_customer.id}')
    return created_customer

@router.post('/anonymous', response_model=schemas.Customer)
def create_anonymous_customer(db: Session = Depends(get_db)) -> schemas.Customer:
    """Cria um novo cliente anônimo.

    Args:
        db (Session): A sessão do banco de dados.

    Returns:
        schemas.Customer: O cliente anônimo criado.
    """
    logger.info('Criando cliente anônimo')
    anonymous_customer = repository.create_anonymous_customer(db)
    logger.info(f'Cliente anônimo criado com ID: {anonymous_customer.id}')
    return anonymous_customer

@router.post('/identify', response_model=schemas.Customer)
def identify_customer(cpf: schemas.CPFIdentify, db: Session = Depends(get_db)) -> schemas.Customer:
    """Identifica um cliente pelo CPF.

    Args:
        cpf (schemas.CPFIdentify): O CPF para identificar o cliente.
        db (Session): A sessão do banco de dados.

    Raises:
        HTTPException: Se o cliente com o CPF fornecido não for encontrado.

    Returns:
        schemas.Customer: O cliente identificado.
    """
    logger.info(f'Identificando cliente com CPF: {cpf.cpf}')
    db_customer = repository.get_customer_by_cpf(db, cpf=cpf.cpf)
    if db_customer is None:
        logger.warning(f'Cliente com CPF {cpf.cpf} não encontrado')
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    return db_customer

#@router.get('/{customer_id}', response_model=schemas.Customer)
#def read_customer(customer_id: str, db: Session = Depends(get_db)) -> schemas.Customer:
#    """Recupera um cliente pelo ID.
#
#    Args:
#        customer_id (str): O ID do cliente para recuperar.
#        db (Session): A sessão do banco de dados.
#
#    Raises:
#        HTTPException: Se o formato do ID do cliente for inválido ou se o cliente não for encontrado.
#
#    Returns:
#        schemas.Customer: Os dados do cliente.
#    """
#    logger.info(f'Buscando cliente com ID: {customer_id}')
#    try:
#        customer_id_int = customer_id
#    except (ValueError, IndexError):
#        logger.warning(f'Formato inválido de ID de cliente: {customer_id}')
#        raise HTTPException(status_code=400, detail='Formato de ID de cliente inválido')
#
#    db_customer = repository.get_customer(db, customer_id=customer_id_int)
#    if db_customer is None:
#        logger.warning(f'Cliente com ID {customer_id} não encontrado')
#        raise HTTPException(status_code=404, detail='Cliente não encontrado')
#    return db_customer
#
#@router.get('', response_model=List[schemas.Customer])
#def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Customer]:
#    """Recupera uma lista de clientes com paginação.
#
#    Args:
#        skip (int): O número de registros a serem ignorados.
#        limit (int): O número máximo de registros a serem retornados.
#        db (Session): A sessão do banco de dados.
#
#    Returns:
#        List[schemas.Customer]: Uma lista de clientes.
#    """
#    logger.info(f'Buscando clientes com skip: {skip}, limit: {limit}')
#    customers = repository.get_customers(db, skip=skip, limit=limit)
#    return customers
