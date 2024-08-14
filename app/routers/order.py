from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
from ..services import security, repository
from ..db.database import get_db
from ..model import schemas
from ..tools.logging import logger

router = APIRouter()

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info("Create order endpoint called")
    try:
        db_order = repository.create_order(db=db, order=order)
        logger.info("Order created successfully")
        return db_order
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: str, update_data: schemas.UpdateOrderStatus, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info(f"Update order status endpoint called for order ID: {order_id} with status: {update_data.status}")
    try:
        order_id_int = order_id
    except (ValueError, IndexError):
        logger.warning(f"Invalid order ID format: {order_id}")
        raise HTTPException(status_code=400, detail="Invalid order ID format")

    try:
        db_order = repository.update_order_status(db, order_id=order_id_int, status=update_data.status)
        if db_order is None:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        logger.info(f"Order ID {order_id} status updated to {update_data.status}")
        return db_order
    except Exception as e:
        logger.error(f"Error updating order status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=Dict[str, List[schemas.OrderResponse]])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info("Read orders endpoint called")
    try:
        orders = repository.get_orders(db, skip=skip, limit=limit)
        logger.info("Orders fetched successfully")
        return {"orders": orders}
    except Exception as e:
        logger.error(f"Error fetching orders: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{order_id}", response_model=schemas.OrderCustomerView)
def read_order(order_id: str, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info(f"Read order endpoint called for order_id: {order_id}")
    try:
        order_id_int = order_id
    except (ValueError, IndexError):
        logger.warning(f"Invalid order ID format: {order_id}")
        raise HTTPException(status_code=400, detail="Invalid order ID format")

    try:
        db_order = repository.get_order(db, order_id=order_id_int)
        if db_order is None:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        logger.info(f"Order fetched successfully for order_id: {order_id}")
        return db_order
    except Exception as e:
        logger.error(f"Error fetching order: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/checkout", response_model=schemas.OrderResponse)
def fake_checkout(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: schemas.Customer = Depends(security.get_current_user)):
    logger.info("Fake checkout endpoint called")
    try:
        db_order = repository.create_order(db=db, order=order)
        logger.info("Checkout order created successfully")
        return db_order
    except Exception as e:
        logger.error(f"Error during fake checkout: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
