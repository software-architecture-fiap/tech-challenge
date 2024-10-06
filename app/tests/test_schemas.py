import pytest
from pydantic import ValidationError
from app.model.schemas import CustomerBase, ProductBase

def test_customer_base_initialization():
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "cpf": "123.456.789-00"
    }
    customer = CustomerBase(**customer_data)
    assert customer.name == "John Doe"
    assert customer.email == "john.doe@example.com"
    assert customer.cpf == "123.456.789-00"

# Test scenario for customer - optional fields
def test_customer_base_optional_fields():
    customer_data = {}
    customer = CustomerBase(**customer_data)
    assert customer.name is None
    assert customer.email is None
    assert customer.cpf is None

# Test scenario for customer - valid data
def test_customer_base_valid_data():
    customer_data = {
        "name": "John Doe",
        "email": "john@abc.com",
        "cpf": "123.456.789-00"
    }
    customer = CustomerBase(**customer_data)
    assert customer.name == "John Doe"
    assert customer.email == "john@abc.com"
    assert customer.cpf == "123.456.789-00"

# Test scenario for customer - invalid data name
def test_customer_base_invalid_name():
    customer_data = {
        "name": 123,
        "email": "abc@abc.com",
        "cpf": "123.456.789-00"
    }
    with pytest.raises(ValidationError):
        CustomerBase(**customer_data)

# Test scenario for customer - invalid data email
def test_customer_base_invalid_email():
    customer_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "cpf": "123.456.789-00"
    }
    with pytest.raises(ValidationError):
        CustomerBase(**customer_data)

def test_product_base_initialization():
    product_data = {
        "name": "Chocolate Cake",
        "description": "A delicious chocolate cake",
        "price": 150.00,
        "category": "Dessert"
    }
    product = ProductBase(**product_data)
    assert product.name == "Chocolate Cake"
    assert product.description == "A delicious chocolate cake"
    assert product.price == pytest.approx(150.00)
    assert product.category == "Dessert"

# Test scenario for product - missing required fields
def test_product_base_missing_fields():
    product_data = {
        "description": "A delicious chocolate cake",
        "price": 150.00,
        "category": "Dessert"
    }
    with pytest.raises(ValidationError):
        ProductBase(**product_data)

# Test scenario for invalid price type
def test_product_base_invalid_price():
    product_data = {
        "name": "Hamburger",
        "description": "A delicious hamburger",
        "price": "ten dollars",
        "category": "Lunch"
    }
    with pytest.raises(ValidationError):
        ProductBase(**product_data)

# Test scenario for valid data
def test_product_base_valid_data():
    product_data = {
        "name": "Fries",
        "description": "A delicious fries",
        "price": 9.99,
        "category": "Snacks"
    }
    product = ProductBase(**product_data)
    assert product.name == "Fries"
    assert product.description == "A delicious fries"
    assert product.price == pytest.approx(9.99)
    assert product.category == "Snacks"

# Test scenario for invalid category type
def test_product_base_invalid_category():
    product_data = {
        "name": "Juice",
        "description": "A delicious juice",
        "price": 8.99,
        "category": 123
    }
    with pytest.raises(ValidationError):
        ProductBase(**product_data)