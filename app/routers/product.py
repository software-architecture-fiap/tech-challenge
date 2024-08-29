from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import database
from ..model import models, schemas
from ..services import repository, security

router = APIRouter()


@router.post('/', response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
):
    # Buscar a categoria no banco de dados
    db_category = repository.get_category(db, category_id=product.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    # Criar o produto associando a categoria correta
    db_product = models.Product(
        name=product.name, description=product.description, price=product.price, category_id=db_category.id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Retornar o produto criado
    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_category.name,
    )
    return product_response


@router.get('/', response_model=Dict[str, List[schemas.Product]])
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
):
    products = repository.get_products(db, skip=skip, limit=limit)
    categorized_products = repository.categorize_products(products)
    return categorized_products


@router.get('/{product_id}', response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
):
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
    return product_response


@router.put('/{product_id}', response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
):
    db_product = repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    # Buscar a categoria no banco de dados
    db_category = repository.get_category(db, category_id=product.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')

    # Atualizar o produto associando a categoria correta
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category_id = db_category.id

    db.commit()
    db.refresh(db_product)

    # Retornar o produto atualizado
    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_category.name,
    )
    return product_response


@router.delete('/{product_id}', response_model=schemas.Product)
def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user),
):
    db_product = repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    # Carregar todos os dados necessários antes de deletar
    product_response = schemas.Product(
        id=str(db_product.id),
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=db_product.category.name,
    )

    repository.delete_product(db=db, product_id=product_id)
    return product_response
