from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
import schemas
import crud
from api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseUsers)
def read_userss(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.users.get_multi_where_array(db=db)
    count = crud.users.get_count_where_array(db=db)
    response = schemas.ResponseUsers(**{'count': count, 'data': jsonable_encoder(users)})
    return response


@router.post('/', response_model=schemas.Users)
def create_users(
        *,
        db: Session = Depends(deps.get_db),
        users_in: schemas.UsersCreate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Create new users.
    """
    if crud.users.is_superuser(current_user):
        users = crud.users.create(db=db, obj_in=users_in)
    else:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    return users


@router.put('/', response_model=schemas.Users)
def update_users(
        *,
        db: Session = Depends(deps.get_db),
        users_id: int,
        users_in: schemas.UsersUpdate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Update an users.
    """
    users = crud.users.get(db=db, id=users_id)
    if not users:
        raise HTTPException(status_code=404, detail='Users not found')
    users = crud.users.update(db=db, db_obj=users, obj_in=users_in)
    return users


@router.get('/by_id/', response_model=schemas.Users)
def read_users(
        *,
        db: Session = Depends(deps.get_db),
        users_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Get users by ID.
    """
    users = crud.users.get(db=db, id=users_id)
    if not users:
        raise HTTPException(status_code=404, detail='Users not found')
    return users


@router.delete('/', response_model=schemas.Users)
def delete_users(
        *,
        db: Session = Depends(deps.get_db),
        users_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an users.
    """
    users = crud.users.get(db=db, id=users_id)
    if not users:
        raise HTTPException(status_code=404, detail='Users not found')
    users = crud.users.remove(db=db, id=users_id)
    return users
