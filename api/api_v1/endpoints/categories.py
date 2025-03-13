from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
import schemas
import crud
from api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseCategories)
def read_categories(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve categories.
    """
    categories = crud.categories.get_multi(db=db)
    count = crud.categories.get_count(db=db)
    response = schemas.ResponseCategories(**{'count': count, 'data': jsonable_encoder(categories)})
    return response


@router.post('/', response_model=schemas.Categories)
def create_categories(
        *,
        db: Session = Depends(deps.get_db),
        categories_in: schemas.CategoriesCreate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Create new categories.
    """
    if crud.users.is_admin(current_user):
        categories = crud.categories.create(db=db, obj_in=categories_in)
    else:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    return categories


@router.put('/', response_model=schemas.Categories)
def update_categories(
        *,
        db: Session = Depends(deps.get_db),
        categories_id: int,
        categories_in: schemas.CategoriesUpdate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Update an categories.
    """
    categories = crud.categories.get(db=db, id=categories_id)
    if not categories:
        raise HTTPException(status_code=404, detail='Categories not found')

    if crud.users.is_admin(current_user):
        categories = crud.categories.update(db=db, db_obj=categories, obj_in=categories_in)
    else:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    return categories


@router.get('/by_id/', response_model=schemas.Categories)
def read_categories(
        *,
        db: Session = Depends(deps.get_db),
        categories_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Get categories by ID.
    """
    categories = crud.categories.get(db=db, id=categories_id)
    if not categories:
        raise HTTPException(status_code=404, detail='Categories not found')
    return categories


@router.delete('/')
def delete_categories(
        *,
        db: Session = Depends(deps.get_db),
        categories_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an categories.
    """
    categories = crud.categories.get(db=db, id=categories_id)
    if not categories:
        raise HTTPException(status_code=404, detail='Categories not found')

    if crud.users.is_admin(current_user):
        categories = crud.categories.remove(db=db, id=categories_id)
    else:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    return "deleted"
