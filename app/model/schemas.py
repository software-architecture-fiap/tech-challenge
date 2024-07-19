from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    cpf: str
    password: str

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: str
    user_agent: str
    ip_address: str
    os: str
    browser: str
    device: str
    comments: Optional[str] = None

class OrderProductBase(BaseModel):
    product_id: int
    comment: Optional[str] = None

class OrderProductCreate(OrderProductBase):
    pass

class OrderProduct(OrderProductBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: str
    user_agent: str
    ip_address: str
    os: str
    browser: str
    device: str
    comments: Optional[str] = None

class OrderCreate(OrderBase):
    customer_id: int
    products: List[OrderProductCreate]

class Order(OrderBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    order_products: List[OrderProduct]

    class Config:
        orm_mode = True

class UpdateOrderStatus(BaseModel):
    status: str
    