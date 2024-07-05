from pydantic import BaseModel
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
    customer_id: int
    status: str

class OrderCreate(OrderBase):
    products: List[int]

class Order(OrderBase):
    id: int
    class Config:
        from_attributes = True
