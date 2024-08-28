import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from dotenv import load_dotenv
from jose import jwt
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..model import models, schemas
from ..tools.logging import logger
from . import security

load_dotenv()


def create_token(db: Session, token: str, user_id: int):
    logger.info(f"Creating token for user ID: {user_id}")
    db_token = models.Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    logger.debug(f"Token created: {db_token.token}")
    return db_token


def mark_token_as_used(db: Session, token: str):
    logger.info(f"Marking token as used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token:
        db_token.is_used = True
        db.commit()
        db.refresh(db_token)
        logger.debug(f"Token marked as used: {token}")
    else:
        logger.warning(f"Token not found: {token}")
    return db_token


def is_token_used(db: Session, token: str):
    logger.debug(f"Checking if token is used: {token}")
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token and db_token.is_used:
        logger.debug(f"Token is used: {token}")
        return True
    logger.debug(f"Token is not used: {token}")
    return False


def create_access_token(data: dict, expires_delta: timedelta):
    logger.debug("Creating access token")
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
    logger.debug(f"Creating user with email: {user.email}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Customer(name=user.name, email=user.email, cpf=user.cpf, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user


def create_anonymous_customer(db: Session):
    logger.debug("Creating anonymous customer")
    anonymous_customer = models.Customer(
        name="Anonymous",
        email=None,
        cpf=None,
        hashed_password=None
    )
    db.add(anonymous_customer)
    db.commit()
    db.refresh(anonymous_customer)
    logger.info(f"Anonymous customer created with ID: {anonymous_customer.id}")
    return anonymous_customer


def get_customer_by_cpf(db: Session, cpf: str):
    logger.debug(f"Fetching customer with CPF: {cpf}")
    return db.query(models.Customer).filter(models.Customer.cpf == cpf).first()


def create_admin_user(db: Session):
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_cpf = os.getenv("ADMIN_CPF")
        admin_name = os.getenv("ADMIN_NAME")

        if not all([admin_email, admin_password, admin_cpf, admin_name]):
            logger.error("Admin user details are not set in environment variables.")
            return

        logger.debug(f"Admin email: {admin_email}, Admin name: {admin_name}")

        user = db.query(models.Customer).filter(models.Customer.email == admin_email).first()
        if not user:
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
            logger.debug(f"Admin user created with email: {admin_email}")
        else:
            logger.debug(f"Admin user already exists with email: {admin_email}")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")


def get_customers_count(db: Session):
    logger.info("Fetching total count of customers")
    return db.query(models.Customer).count()


def get_customer(db: Session, customer_id: int):
    logger.debug(f"Fetching customer with ID: {customer_id}")
    try:
        return db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        return None


def get_customers(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching customers with skip: {skip}, limit: {limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    logger.debug(f"Creating customer with email: {customer.email}")
    db_customer = models.Customer(name=customer.name, email=customer.email, cpf=customer.cpf)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    logger.info(f"Customer created with ID: {db_customer.id}")
    return db_customer


def categorize_products(products: List[models.Product]) -> Dict[str, List[schemas.Product]]:
    categorized_products = {}
    for product in products:
        product_data = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category.name
        }

        if product.category.name not in categorized_products:
            categorized_products[product.category.name] = []

        categorized_products[product.category.name].append(schemas.Product(**product_data))

    return categorized_products


def get_product(db: Session, product_id: int):
    logger.debug(f"Fetching product with ID: {product_id}")
    try:
        return db.query(models.Product).filter(models.Product.id == product_id).first()
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        return None


def get_products(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching products with skip: {skip}, limit: {limit}")
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    logger.debug(f"Creating product with name: {product.name}")

    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    logger.info(f"Product created with ID: {db_product.id}")

    return db_product


def update_product(db: Session, db_product: models.Product, product: schemas.ProductCreate):
    logger.debug(f"Updating product with name: {product.name}")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db.commit()
    db.refresh(db_product)
    logger.info(f"Product updated with ID: {db_product.id}")
    return db_product


def delete_product(db: Session, product_id: int):
    logger.debug(f"Deleting product with ID: {product_id}")
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            logger.info(f"Product deleted: {db_product.name} - Category: {db_product.category}")
        else:
            logger.warning(f"Product not found: ID {product_id}")
        return db_product
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return None


def create_order(db: Session, order: schemas.OrderCreate):
    logger.debug(f"Creating order for customer ID: {order.customer_id}")
    try:
        customer_id_int = order.customer_id
        db_order = models.Order(
            status=order.status,
            user_agent=order.user_agent,
            ip_address=order.ip_address,
            os=order.os,
            browser=order.browser,
            device=order.device,
            comments=order.comments,
            customer_id=customer_id_int,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        logger.info(f"Order created with ID: {db_order.id}")

        for product in order.products:
            product_id_int = product.product_id
            db_order_product = models.OrderProduct(
                order_id=db_order.id,
                product_id=product_id_int,
                comment=product.comment
            )
            db.add(db_order_product)
            db.commit()
            db.refresh(db_order_product)
            logger.info(f"Product {db_order_product.product_id} added to order {db_order.id}")

        create_tracking(db, db_order.id, db_order.status)

        return db_order
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        raise


def update_order_status(db: Session, order_id: int, status: str):
    logger.debug(f"Updating order status for order ID: {order_id} to {status}")
    try:
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if db_order:
            db_order.status = status
            db_order.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(db_order)
            logger.info(f"Order ID {db_order.id} status updated to {status}")
            create_tracking(db, db_order.id, status)
        return db_order
    except Exception as e:
        logger.error(f"Error updating order status: {e}", exc_info=True)
        raise


def create_tracking(db: Session, order_id: int, status: str):
    logger.debug(f"Creating tracking entry for order ID: {order_id} with status: {status}")
    try:
        db_tracking = models.Tracking(
            order_id=order_id,
            status=status,
            created_at=datetime.now(timezone.utc)
        )
        db.add(db_tracking)
        db.commit()
        db.refresh(db_tracking)
        logger.info(f"Tracking entry created with ID: {db_tracking.id}")
        return db_tracking
    except Exception as e:
        logger.error(f"Error creating tracking entry: {e}", exc_info=True)
        raise


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching orders with skip: {skip}, limit: {limit}")
    try:
        orders = db.query(models.Order).offset(skip).limit(limit).all()
        logger.info("Orders fetched successfully")
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders: {e}", exc_info=True)
        raise


def get_order(db: Session, order_id: int):
    logger.debug(f"Fetching order with ID: {order_id}")
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        logger.info("Order fetched successfully")
        return order
    except Exception as e:
        logger.error(f"Error fetching order: {e}", exc_info=True)
        raise


def get_categories(db: Session, skip: int = 0, limit: int = 10) -> List[schemas.Category]:
    logger.debug(f"Fetching categories with skip: {skip}, limit: {limit}")

    categories = db.execute(
        text("SELECT id, name FROM categories LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).fetchall()

    category_list = []
    for category in categories:
        category_id = category.id
        products = db.execute(
            text("SELECT id, name, description, price FROM products WHERE category_id = :category_id"),
            {"category_id": category_id}
        ).fetchall()

        product_list = [
            schemas.Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                category=category.name
            )
            for product in products
        ]

        category_list.append(schemas.Category(
            id=category.id,
            name=category.name,
            products=product_list
        ))

    return category_list


def get_category_with_products(db: Session, category_id: int):
    logger.debug(f"Fetching category with ID: {category_id}")
    try:
        result = db.execute(
            text("SELECT * FROM categories WHERE id = :category_id"),
            {"category_id": category_id}
        ).fetchone()
        if result:
            products = db.execute(
                text("SELECT * FROM products WHERE category_id = :category_id"),
                {"category_id": category_id}
            ).fetchall()

            product_list = [schemas.Product(**dict(product)) for product in products]
            return schemas.Category(**dict(result), products=product_list)
    except Exception as e:
        logger.error(f"Error fetching category: {e}")
        return None


def get_category(db: Session, category_id: int):
    logger.debug(f"Fetching category with ID: {category_id}")
    try:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            return category
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching category: {e}")
        return None


def update_category(db: Session, db_category: models.Category, category: schemas.CategoryCreate):
    logger.debug(f"Updating category with ID: {db_category.id}")
    try:
        db_category.id = category.id
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        return None


def delete_category(db: Session, db_category: models.Category):
    logger.debug(f"Deleting category with ID: {db_category.id}")
    try:
        db.delete(db_category)
        db.commit()
        return db_category
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        return None
