from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..model import schemas
from ..services import repository
from ..db.database import get_db
from ..tools.logging import logger

router = APIRouter()

@router.post("/admin", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating customer with email: {customer.email}")
    db_customer = repository.get_user_by_email(db, email=customer.email)
    if db_customer:
        logger.warning(f"Customer with email {customer.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    created_customer = repository.create_user(db=db, user=customer)
    logger.info(f"Customer created with ID: {created_customer.id}")
    return created_customer

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with ID: {customer_id}")
    db_customer = repository.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.get("/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching customers with skip: {skip}, limit: {limit}")
    customers = repository.get_customers(db, skip=skip, limit=limit)
    return customers

@router.post("/identify", response_model=schemas.Customer)
def identify_customer(cpf: schemas.CPFIdentify, db: Session = Depends(get_db)):
    logger.info(f"Identifying customer with CPF: {cpf.cpf}")
    db_customer = repository.get_customer_by_cpf(db, cpf=cpf.cpf)
    if db_customer is None:
        logger.warning(f"Customer with CPF {cpf.cpf} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/register", response_model=schemas.Customer)
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering customer with email: {customer.email}")
    db_customer = repository.get_user_by_email(db, email=customer.email)
    if db_customer:
        logger.warning(f"Customer with email {customer.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    created_customer = repository.create_user(db=db, user=customer)
    logger.info(f"Customer registered with ID: {created_customer.id}")
    return created_customer

@router.post("/anonymous", response_model=schemas.Customer)
def create_anonymous_customer(db: Session = Depends(get_db)):
    logger.info("Creating anonymous customer")
    anonymous_customer = repository.create_anonymous_customer(db)
    logger.info(f"Anonymous customer created with ID: {anonymous_customer.id}")
    return anonymous_customer

