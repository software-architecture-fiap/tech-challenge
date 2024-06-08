from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas, database, security
from ..database import get_db

router = APIRouter()

@router.post("/admin", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    if crud.get_customers_count(db) == 0:
        # Permite a criação do primeiro cliente sem autenticação
        return crud.create_user(db=db, user=customer)
    else:
        raise HTTPException(status_code=400, detail="Use the signup endpoint to create a customer")

# Endpoint de signup para clientes autenticados
@router.post("/signup", response_model=schemas.Customer)
def signup_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_user = crud.get_user_by_email(db, email=customer.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=customer)

@router.get("/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(database.get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer
