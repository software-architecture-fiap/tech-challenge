from typing import Dict, List, Union, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..db import database
from ..model import models, schemas
from ..services import repository
from ..tools.logging import logger

router = APIRouter()

@router.get('/', response_model=Union[Dict[str, List[schemas.Category]], schemas.Category])
def list_or_get_category(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
) -> Union[Dict[str, List[schemas.Category]], schemas.Category]:
    """
    Lista categorias com paginação ou retorna os detalhes de uma categoria específica pelo ID.

    Args:
        category_id (Optional[int]): ID da categoria a ser recuperada. Se não fornecido, retorna uma lista de categorias.
        skip (int): Número de categorias a serem ignoradas (pular). Padrão é 0.
        limit (int): Número máximo de categorias a serem retornadas. Padrão é 10.
        db (Session): Instância de sessão do banco de dados.

    Returns:
        Union[Dict[str, List[schemas.Category]], schemas.Category]: Detalhes de uma categoria ou uma lista de categorias.

    Raises:
        HTTPException: Se a categoria solicitada não for encontrada.
    """
    if category_id is not None:
        logger.info(f'Recebido ID da categoria: {category_id}')
        db_category = repository.get_category(db, category_id=category_id)
        if not db_category:
            logger.error(f'Categoria não encontrada para ID: {category_id}')
            raise HTTPException(status_code=404, detail='Categoria não encontrada')

        category_response = schemas.Category(
            id=str(db_category.id),
            name=db_category.name,
            products=[
                schemas.Product(
                    id=str(product.id),
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category=db_category.name,
                )
                for product in db_category.products
            ],
        )

        logger.info(f'Retorno da categoria: {category_response}')
        return category_response

    logger.info('Listando categorias com paginação')
    categories = repository.get_categories(db, skip=skip, limit=limit)
    return {'categories': categories}

@router.post('/', response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
):
    """
    Cria uma nova categoria.

    Este endpoint cria uma nova categoria com base nos dados fornecidos.

    Args:
        category (schemas.CategoryCreate): Dados da nova categoria a ser criada.
        db (Session, opcional): Instância de sessão do banco de dados.

    Returns:
        schemas.Category: A categoria criada.

    Raises:
        HTTPException: Se uma categoria com o mesmo nome já existir ou se ocorrer um erro interno.
    """
    logger.info(f'Recebido pedido para criar a categoria com nome: {category.name}')

    try:
        existing_category = db.query(models.Category).filter(and_(models.Category.name == category.name)).first()
        if existing_category:
            logger.warning(f"Categoria com o nome '{category.name}' já existe")
            raise HTTPException(status_code=400, detail='Categoria já existe')

        db_category = models.Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        logger.info(f'Categoria criada com sucesso com ID: {db_category.id}')

        return schemas.Category(id=db_category.id, name=db_category.name, products=[])

    except Exception as e:
        logger.error(f'Erro ao criar categoria: {e}')
        raise HTTPException(status_code=500, detail='Erro interno do servidor')

@router.patch('/{category_id}', response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
):
    """
    Atualiza uma categoria existente.

    Este endpoint atualiza os detalhes de uma categoria existente identificada pelo ID fornecido.

    Args:
        category_id (int): ID da categoria a ser atualizada.
        category (schemas.CategoryCreate): Novos dados da categoria.
        db (Session, opcional): Instância de sessão do banco de dados.

    Returns:
        schemas.Category: A categoria atualizada.

    Raises:
        HTTPException: Se a categoria não for encontrada.
    """
    db_category = repository.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)

    category_response = schemas.Category(
        id=str(db_category.id),
        name=db_category.name,
        products=[
            schemas.Product(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=product.price,
                category=db_category.name,
            )
            for product in db_category.products
        ],
    )

    return category_response

@router.put('/{category_id}', response_model=schemas.Category)
def delete_category(
    category_id: str,
    db: Session = Depends(database.get_db),
):
    """
    Remove uma categoria pelo ID.

    Este endpoint remove uma categoria identificada pelo ID fornecido.

    Args:
        category_id (str): ID da categoria a ser removida.
        db (Session, opcional): Instância de sessão do banco de dados.

    Returns:
        schemas.Category: A categoria removida.

    Raises:
        HTTPException: Se a categoria não for encontrada ou se o formato do ID for inválido.
    """
    try:
        category_id_int = int(category_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail='Formato de ID de categoria inválido')

    db_category = repository.get_category(db, category_id=category_id_int)
    if db_category is None:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')

    repository.delete_category(db, db_category=db_category)
    return db_category

#@router.get('/', response_model=Dict[str, List[schemas.Category]])
#def list_categories(
#    skip: int = 0,
#    limit: int = 10,
#    db: Session = Depends(database.get_db),
#):
#    """
#    Lista todas as categorias com paginação.
#
#    Este endpoint retorna uma lista de categorias com base nos parâmetros de paginação fornecidos.
#
#    Args:
#        skip (int): Número de categorias a serem ignoradas (pular). Padrão é 0.
#        limit (int): Número máximo de categorias a serem retornadas. Padrão é 10.
#        db (Session, opcional): Instância de sessão do banco de dados.
#
#    Returns:
#        dict: Um dicionário contendo uma lista de categorias.
#    """
#    categories = repository.get_categories(db, skip=skip, limit=limit)
#    return {'categories': categories}
#
#@router.get('/{category_id}', response_model=schemas.Category)
#def get_category(
#    category_id: int,
#    db: Session = Depends(database.get_db),
#):
#    """
#    Obtém uma categoria específica pelo ID.
#
#    Este endpoint retorna os detalhes de uma categoria específica identificada pelo ID fornecido.
#
#    Args:
#        category_id (int): ID da categoria a ser recuperada.
#        db (Session, opcional): Instância de sessão do banco de dados.
#
#    Returns:
#        schemas.Category: Detalhes da categoria solicitada.
#
#    Raises:
#        HTTPException: Se a categoria não for encontrada.
#    """
#    logger.info(f'Recebido ID da categoria: {category_id}')
#
#    db_category = repository.get_category(db, category_id=category_id)
#
#    if not db_category:
#        logger.error(f'Categoria não encontrada para ID: {category_id}')
#        raise HTTPException(status_code=404, detail='Categoria não encontrada')
#
#    category_response = schemas.Category(
#        id=str(db_category.id),
#        name=db_category.name,
#        products=[
#            schemas.Product(
#                id=str(product.id),
#                name=product.name,
#                description=product.description,
#                price=product.price,
#                category=db_category.name,
#            )
#            for product in db_category.products
#        ],
#    )
#
#    logger.info(f'Retorno da categoria: {category_response}')
#    return category_response
