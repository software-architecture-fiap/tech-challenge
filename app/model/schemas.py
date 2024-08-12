from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class CustomerBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: Optional[str] = None

class Customer(CustomerBase):
    id: str  
    
    class Config:
        from_attributes = True

class CPFIdentify(BaseModel):
    cpf: str

class Token(BaseModel):
    access_token: str
    customer_id: str  

class TokenData(BaseModel):
    username: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

    model_config = ConfigDict(from_attributes=True)

class Product(BaseModel):
    name: str
    description: str
    price: float
    category: str

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str  
    
    class Config:
        model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: str  
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
    product_id: str  
    comment: Optional[str] = None

class OrderProductCreate(OrderProductBase):
    pass

class OrderProduct(OrderProductBase):
    id: str  

    class Config:
        from_attributes = True

class OrderCreate(OrderBase):
    customer_id: str  
    products: List[OrderProductCreate]

class Order(OrderBase):
    id: str  
    customer_id: str  
    created_at: datetime
    updated_at: datetime
    order_products: List[OrderProduct] = []
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: str  
    customer_id: str  
    class Config:
        from_attributes = True

class OrderCustomerView(BaseModel):
    id: str  
    customer_id: str  
    status: str
    class Config:
        from_attributes = True

class TrackingCreate(BaseModel):
    status: str
    order_id: str  

class Tracking(BaseModel):
    id: str  
    order_id: str  
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class UpdateOrderStatus(BaseModel):
    status: str
