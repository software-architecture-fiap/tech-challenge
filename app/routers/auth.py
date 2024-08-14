from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ..services import security
from ..model import schemas
from ..services import repository
from ..db.database import get_db
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from ..tools.logging import logger

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = repository.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": security.int_to_short_id(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"Token created for user ID: {user.id}")
    return {"access_token": f'bearer {access_token}', "customer_id": str(security.int_to_short_id(user.id))}
