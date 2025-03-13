from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
import crud
from api import deps
from core import security
from core.config import settings

router = APIRouter()


@router.post("/signup", response_model=schemas.Token)
def signup(
        *,
        db: Session = Depends(deps.get_db),
        users_in: schemas.UsersCreate,
) -> Any:
    """
    Create new users.
    """
    user = crud.users.create(db=db, obj_in=users_in)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = security.create_access_token(
        data={"id": str(user.id), "username": user.username},
        expires_delta=access_token_expires,
    )

    return {"access_token": token, "token_type": "Bearer", "role": user.role}


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.users.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = security.create_access_token(
        data={"id": str(user.id), "username": form_data.username},
        expires_delta=access_token_expires,
    )
    token_data = deps.get_user(token)
    user = crud.users.get(db=db, id=token_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"access_token": token, "token_type": "Bearer", "role": user.role}


@router.post("/verify-token", response_model=schemas.Users)
def verify_token(current_user: models.Users = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    expired_date = datetime(year=2025, month=8, day=31)
    current_date = datetime.now()
    if current_date >= expired_date:
        raise HTTPException(status_code=400, detail="Expired Version")
    return current_user
