from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, security

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    return crud.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
