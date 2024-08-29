from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db.database import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship('Order', back_populates='customer')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True, default='created')
    user_agent = Column(String)
    ip_address = Column(String)
    os = Column(String)
    browser = Column(String)
    device = Column(String)
    comments = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    order_products = relationship('OrderProduct', back_populates='order')
    tracking = relationship('Tracking', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(String)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(Text)

    order = relationship('Order', back_populates='order_products')
    product = relationship('Product')


class Tracking(Base):
    __tablename__ = 'tracking'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    status = Column(String, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship('Order', back_populates='tracking')


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('customers.id'))

    user = relationship('Customer')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship('Product', back_populates='category')
