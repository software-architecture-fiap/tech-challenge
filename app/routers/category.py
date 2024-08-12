from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session

from ..services import repository
from ..services import security
from ..model import models, schemas
from ..db import database

router = APIRouter()

@router.get("/", response_model=Dict[str, List[schemas.Category]])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    categories = repository.get_categories(db, skip=skip, limit=limit)
    return {"categories": categories}


@router.get("/{category_id}", response_model=schemas.Category)
def list_category(category_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_category = repository.get_category_with_products(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_category = repository.get_categories(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    updated_category = repository.update_category(db, db_category=db_category, category=category)
    return updated_category

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_category = repository.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    repository.delete_category(db, db_category=db_category)
    return db_category
