from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
from ..services import repository, security
from ..tools.logging import logger
from ..model import schemas, models
from ..db import database

router = APIRouter()

@router.get("/", response_model=Dict[str, List[schemas.Category]])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    categories = repository.get_categories(db, skip=skip, limit=limit)
    return {"categories": categories}

@router.get("/{category_id}", response_model=schemas.Category)
def list_category(category_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info(f"Received category ID: {category_id}")
    
    db_category = repository.get_category(db, category_id=category_id)
    
    if not db_category:
        logger.error(f"Category not found for ID: {category_id}")
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Montar a resposta
    category_response = schemas.Category(
        id=str(db_category.id),
        name=db_category.name,
        products=[schemas.Product(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=product.price,
            category=db_category.name
        ) for product in db_category.products]
    )
    
    logger.info(f"Returning category: {category_response}")
    return category_response

@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.Customer = Depends(security.get_current_user)
):
    logger.info(f"Received request to create category with name: {category.name}")
    
    try:
        # Verificar se uma categoria com o mesmo nome já existe
        existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()
        if existing_category:
            logger.warning(f"Category with name '{category.name}' already exists")
            raise HTTPException(status_code=400, detail="Category already exists")
        
        # Criar uma nova categoria
        db_category = models.Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        logger.info(f"Category created successfully with ID: {db_category.id}")
        
        # Retornar a categoria criada
        return schemas.Category(
            id=db_category.id,
            name=db_category.name,
            products=[]
        )
    
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    # Buscar a categoria existente no banco de dados
    db_category = repository.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Atualizar a categoria
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    
    category_response = schemas.Category(
        id=str(db_category.id),
        name=db_category.name,
        products=[schemas.Product(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=product.price,
            category=db_category.name
        ) for product in db_category.products]
    )
    
    return category_response

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: str, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    try:
        category_id_int = category_id
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid category ID format")

    db_category = repository.get_category(db, category_id=category_id_int)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    repository.delete_category(db, db_category=db_category)
    return db_category
