from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session

from ..services import repository
from ..services import security
from ..model import schemas
from ..db import database

router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    return repository.create_product(db=db, product=product)

@router.get("/", response_model=Dict[str, List[schemas.Product]])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    products = repository.get_products(db, skip=skip, limit=limit)
    categorized_products = repository.categorize_products(products)
    return categorized_products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: str, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        product_id_int = security.short_id_to_int(product_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    db_product = repository.get_product(db, product_id=product_id_int)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: str, product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        product_id_int = security.short_id_to_int(product_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    db_product = repository.get_product(db, product_id=product_id_int)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = repository.update_product(db, db_product=db_product, product=product)
    return updated_product

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(product_id: str, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        product_id_int = security.short_id_to_int(product_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    db_product = repository.get_product(db, product_id=product_id_int)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return repository.delete_product(db=db, product_id=product_id_int)
