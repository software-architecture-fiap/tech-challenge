from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CustomerBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: Optional[str] = None

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

class CPFIdentify(BaseModel):
    cpf: str


class Token(BaseModel):
    access_token: str
    token_type: str
    customer_id: int

class TokenData(BaseModel):
    username: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    products: List[Product] = []
    
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
        from_attributes = True

class OrderCreate(OrderBase):
    customer_id: int
    products: List[OrderProductCreate]

class Order(OrderBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    order_products: List[OrderProduct] = []
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    class Config:
        from_attributes = True

class OrderCustomerView(BaseModel):
    id: int
    customer_id: int
    status: str
    class Config:
        from_attributes = True

class TrackingCreate(BaseModel):
    status: str
    order_id: int

class Tracking(BaseModel):
    id: int
    order_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class UpdateOrderStatus(BaseModel):
    status: str
    
