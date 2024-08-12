import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
from ..services import repository
from ..services import security
from ..model import schemas
from ..db import database

router = APIRouter()

@router.get("/", response_model=Dict[str, List[schemas.Category]])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    categories = repository.get_categories(db, skip=skip, limit=limit)
    return {"categories": categories}

@router.get("/{category_id}", response_model=schemas.Category)
def list_category(category_id: str, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logging.info(f"Received category ID: {category_id}")
    try:
        category_id_int = security.short_id_to_int(category_id)
        logging.info(f"Decoded short_id '{category_id}' to int ID: {category_id_int}")
    except (ValueError, IndexError) as e:
        logging.error(f"Error decoding short_id: {e}, category_id: {category_id}")
        raise HTTPException(status_code=400, detail="Invalid category ID format")

    db_category = repository.get_category_with_products(db, category_id=category_id_int)
    if db_category is None:
        logging.error(f"Category not found for decoded int ID: {category_id_int}")
        raise HTTPException(status_code=404, detail="Category not found")
    logging.info(f"Found category: {db_category}")
    return db_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: str, category: schemas.CategoryCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        category_id_int = security.short_id_to_int(category_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid category ID format")

    db_category = repository.get_category(db, category_id=category_id_int)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    updated_category = repository.update_category(db, db_category=db_category, category=category)
    return updated_category

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: str, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        category_id_int = security.short_id_to_int(category_id)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid category ID format")

    db_category = repository.get_category(db, category_id=category_id_int)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    repository.delete_category(db, db_category=db_category)
    return db_category
