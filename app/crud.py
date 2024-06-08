from sqlalchemy.orm import Session
from . import models, schemas, security
from jose import jwt
from datetime import datetime, timedelta
from .logging_config import logger

def get_user_by_email(db: Session, email: str):
    logger.info(f"Fetching user with email: {email}")
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers_count(db: Session):
    logger.info("Fetching total count of customers")
    return db.query(models.Customer).count()

def create_user(db: Session, user: schemas.CustomerCreate):
    logger.info(f"Creating user with email: {user.email}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Customer(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user

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
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)
    logger.info("Access token created")
    return encoded_jwt

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
    logger.info(f"Order created with ID: {db_order.id}")
    return db_order
