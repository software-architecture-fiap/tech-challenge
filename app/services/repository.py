from sqlalchemy.orm import Session
from typing import List, Dict
from ..model import models, schemas
from . import security
from ..db.database import SessionLocal
from jose import jwt
from datetime import datetime, timedelta, timezone
from ..tools.logging import logger
import os
from dotenv import load_dotenv as env

env()

def create_token(db: Session, token: str, user_id: int):
    logger.info(f"Creating token for user ID: {user_id}")
    db_token = models.Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    logger.info(f"Token created: {db_token.token}")
    return db_token

def mark_token_as_used(db: Session, token: str):
    logger.info(f"Marking token as used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token:
        db_token.is_used = True
        db.commit()
        db.refresh(db_token)
        logger.info(f"Token marked as used: {token}")
    else:
        logger.warning(f"Token not found: {token}")
    return db_token

def is_token_used(db: Session, token: str):
    logger.info(f"Checking if token is used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token and db_token.is_used:
        logger.info(f"Token is used: {token}")
        return True
    logger.info(f"Token is not used: {token}")
    return False

def create_access_token(data: dict, expires_delta: timedelta):
    logger.info("Creating access token")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)
    logger.info("Access token created")
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    logger.info(f"Fetching user with email: {email}")
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_user(db: Session, user: schemas.CustomerCreate):
    logger.info(f"Creating user with email: {user.email}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Customer(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user

def create_admin_user(db: Session, user: schemas.CustomerCreate):
    logger.info(f"Creating user with email: {user.email}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Customer(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user

def create_admin_user(db: Session):
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_cpf = os.getenv("ADMIN_CPF")
        admin_name = os.getenv("ADMIN_NAME")

        if not all([admin_email, admin_password, admin_cpf, admin_name]):
            logger.error("Admin user details are not set in environment variables.")
            return

        logger.info(f"Admin email: {admin_email}, Admin name: {admin_name}")

        # Check if the user already exists
        user = db.query(models.Customer).filter(models.Customer.email == admin_email).first()
        if not user:
            # Create new admin user
            hashed_password = security.get_password_hash(admin_password)
            admin_user = models.Customer(
                name=admin_name,
                email=admin_email,
                cpf=admin_cpf,
                hashed_password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info(f"Admin user created with email: {admin_email}")
        else:
            logger.info(f"Admin user already exists with email: {admin_email}")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")

def get_customers_count(db: Session):
    logger.info("Fetching total count of customers")
    return db.query(models.Customer).count()

def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer with ID: {customer_id}")
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Fetching customers with skip: {skip}, limit: {limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    logger.info(f"Creating customer with email: {customer.email}")
    db_customer = models.Customer(name=customer.name, email=customer.email, cpf=customer.cpf)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    logger.info(f"Customer created with ID: {db_customer.id}")
    return db_customer

def categorize_products(products: List[schemas.Product]) -> Dict[str, List[schemas.Product]]:
    categorized_products = {}
    for product in products:
        if product.category not in categorized_products:
            categorized_products[product.category] = []
        categorized_products[product.category].append(product)
    return categorized_products

def get_product(db: Session, product_id: int):
    logger.info(f"Fetching product with ID: {product_id}")
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Fetching products with skip: {skip}, limit: {limit}")
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    logger.info(f"Creating product with name: {product.name}")
    db_product = models.Product(name=product.name, description=product.description, price=product.price, category=product.category)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    logger.info(f"Product created with ID: {db_product.id}")
    return db_product

def update_product(db: Session, db_product: models.Product, product: schemas.ProductCreate):
    logger.info(f"Updating product with name: {product.name}")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db.commit()
    db.refresh(db_product)
    logger.info(f"Product updated with ID: {db_product.id}")
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        logger.info(f"Product deleted: {db_product.name} - Category: {db_product.category}")
    else:
        logger.warning(f"Product not found: ID {product_id}")
    return db_product


def get_order(db: Session, order_id: int):
    logger.info(f"Fetching order with ID: {order_id}")
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Fetching orders with skip: {skip}, limit: {limit}")
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    logger.info(f"Creating order for customer ID: {order.customer_id}")
    db_order = models.Order(customer_id=order.customer_id, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for product_id in order.products:
        db_order_product = models.OrderProduct(order_id=db_order.id, product_id=product_id)
        db.add(db_order_product)
    logger.info(f"Order created with ID: {db_order.id}")
    db.commit()
    return db_order
