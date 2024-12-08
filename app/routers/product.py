from typing import Dict, List, Union, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import database
from ..model import models, schemas
from ..services import repository, security
from ..tools.logging import logger

router = APIRouter()

@router.post('', response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.Product:
    """Cria um novo produto com os dados fornecidos.

    Args:
        product (schemas.ProductCreate): Dados para criação do produto.
        db (Session): Sessão do banco de dados.
        current_user (schemas.Customer): Usuário autenticado atualmente.

    Raises:
        HTTPException: Se a categoria não for encontrada.

    Returns:
        schemas.Product: O produto criado com seus detalhes.
    """
    db_category = repository.get_category(db, category_id=product.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    db_product = models.Product(
        name=product.name, description=product.description, price=product.price, category_id=db_category.id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_category.name,
    )
    return product_response

@router.get('', response_model=Union[Dict[str, List[schemas.Product]], schemas.Product])
def read_products_or_product(
    product_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> Union[Dict[str, List[schemas.Product]], schemas.Product]:
    """
    Recupera produtos categorizados ou um produto específico pelo ID.

    Args:
        product_id (Optional[int]): ID do produto a ser recuperado. Se não fornecido, retorna uma lista categorizada.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
        db (Session): Sessão do banco de dados.
        current_user (schemas.Customer): Usuário autenticado atualmente.

    Raises:
        HTTPException: Se o produto não for encontrado.

    Returns:
        Union[Dict[str, List[schemas.Product]], schemas.Product]: Detalhes do produto ou lista de produtos categorizados.
    """
    try:
        if product_id:
            logger.info(f'Buscando produto com ID: {product_id}')
            db_product = repository.get_product(db, product_id=product_id)
            if db_product is None:
                logger.warning(f'Produto com ID {product_id} não encontrado')
                raise HTTPException(status_code=404, detail='Product not found')

            product_response = schemas.Product(
                id=str(db_product.id),
                name=db_product.name,
                description=db_product.description,
                price=db_product.price,
                category=db_product.category.name,
            )
            return product_response

        logger.info(f'Buscando lista de produtos com paginação skip={skip}, limit={limit}')
        products = repository.get_products(db, skip=skip, limit=limit)
        categorized_products = repository.categorize_products(products)
        return categorized_products

    except Exception as e:
        logger.error(f'Erro ao processar a requisição: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail='Erro Interno do Servidor')

@router.patch('/{product_id}', response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.Product:
    """Atualiza um produto existente com os dados fornecidos.

    Args:
        product_id (int): ID do produto a ser atualizado.
        product (schemas.ProductCreate): Novos dados para o produto.
        db (Session): Sessão do banco de dados.
        current_user (schemas.Customer): Usuário autenticado atualmente.

    Raises:
        HTTPException: Se o produto ou a categoria não for encontrado.

    Returns:
        schemas.Product: O produto atualizado com seus detalhes.
    """
    db_product = repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    db_category = repository.get_category(db, category_id=product.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category_id = db_category.id

    db.commit()
    db.refresh(db_product)

    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_category.name,
    )
    return product_response

@router.put('/{product_id}', response_model=schemas.Product)
def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
) -> schemas.Product:
    """Exclui um produto pelo seu ID.

    Args:
        product_id (int): ID do produto a ser excluído.
        db (Session): Sessão do banco de dados.
        current_user (schemas.Customer): Usuário autenticado atualmente.

    Raises:
        HTTPException: Se o produto não for encontrado.

    Returns:
        schemas.Product: Detalhes do produto excluído.
    """
    db_product = repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_product.category.name,
    )

    repository.delete_product(db=db, product_id=product_id)
    return product_response

#@router.get('/', response_model=Dict[str, List[schemas.Product]])
#def read_products(
#    skip: int = 0,
#    limit: int = 10,
#    db: Session = Depends(database.get_db),
#    current_user: schemas.Customer = Depends(security.get_current_user),
#) -> Dict[str, List[schemas.Product]]:
#    """Recupera uma lista de produtos com paginação.
#
#    Args:
#        skip (int): Número de registros a serem ignorados.
#        limit (int): Número máximo de registros a serem retornados.
#        db (Session): Sessão do banco de dados.
#        current_user (schemas.Customer): Usuário autenticado atualmente.
#
#    Returns:
#        Dict[str, List[schemas.Product]]: Um dicionário contendo uma lista de produtos categorizados.
#    """
#    products = repository.get_products(db, skip=skip, limit=limit)
#    categorized_products = repository.categorize_products(products)
#    return categorized_products
#
#@router.get('/{product_id}', response_model=schemas.Product)
#def read_product(
#    product_id: int,
#    db: Session = Depends(database.get_db),
#    current_user: schemas.Customer = Depends(security.get_current_user),
#) -> schemas.Product:
#    """Recupera um produto específico pelo seu ID.
#
#    Args:
#        product_id (int): ID do produto a ser recuperado.
#        db (Session): Sessão do banco de dados.
#        current_user (schemas.Customer): Usuário autenticado atualmente.
#
#    Raises:
#        HTTPException: Se o produto não for encontrado.
#
#    Returns:
#        schemas.Product: Detalhes do produto.
#    """
#    db_product = repository.get_product(db, product_id=product_id)
#    if db_product is None:
#        raise HTTPException(status_code=404, detail='Product not found')
#
#    product_response = schemas.Product(
#        id=str(db_product.id),
#        name=db_product.name,
#        description=db_product.description,
#        price=db_product.price,
#        category=db_product.category.name,
#    )
#    return product_response
#
