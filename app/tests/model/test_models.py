import pytest
from datetime import datetime
from app.model.schemas import Order, OrderProduct

def test_order_initialization():
    order_data = {
        "id": 1,
        "customer_id": 1,
        "status": "Pending",
        "payment_status": "Unpaid",
        "user_agent": "Mozilla/5.0",
        "ip_address": "192.168.1.1",
        "os": "Windows",
        "browser": "Firefox",
        "device": "Desktop",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "order_products": []
    }
    order = Order(**order_data)
    assert order.id == 1
    assert order.customer_id == 1
    assert order.status == "Pending"
    assert order.payment_status == "Unpaid"
    assert order.user_agent == "Mozilla/5.0"
    assert order.ip_address == "192.168.1.1"
    assert order.os == "Windows"
    assert order.browser == "Firefox"
    assert order.device == "Desktop"
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)
    assert order.order_products == []

def test_order_with_products():
    order_product_data = {
        "id": 1,
        "product_id": 1,
        "comment": "Test comment",
        "product": None
    }
    order_product = OrderProduct(**order_product_data)
    
    order_data = {
        "id": 1,
        "customer_id": 1,
        "status": "Pending",
        "payment_status": "Unpaid",
        "user_agent": "Mozilla/5.0",
        "ip_address": "192.168.1.1",
        "os": "Windows",
        "browser": "Firefox",
        "device": "Desktop",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "order_products": [order_product]
    }
    order = Order(**order_data)
    assert len(order.order_products) == 1
    assert order.order_products[0].id == 1
    assert order.order_products[0].product_id == 1
    assert order.order_products[0].comment == "Test comment"