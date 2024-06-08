from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database, security

router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
