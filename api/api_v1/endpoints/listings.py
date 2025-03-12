from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
import schemas
import crud
from api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseListings)
def read_listingss(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve listingss.
    """
    listingss = crud.listings.get_multi_where_array(db=db)
    count = crud.listings.get_count_where_array(db=db)
    response = schemas.ResponseListings(**{'count': count, 'data': jsonable_encoder(listingss)})
    return response


@router.post('/', response_model=schemas.Listings)
def create_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_in: schemas.ListingsCreate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Create new listings.
    """
    if crud.users.is_superuser(current_user):
        listings = crud.listings.create(db=db, obj_in=listings_in)
    else:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    return listings


@router.put('/', response_model=schemas.Listings)
def update_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        listings_in: schemas.ListingsUpdate,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Update an listings.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')
    listings = crud.listings.update(db=db, db_obj=listings, obj_in=listings_in)
    return listings


@router.get('/by_id/', response_model=schemas.Listings)
def read_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Get listings by ID.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')
    return listings


@router.delete('/', response_model=schemas.Listings)
def delete_listings(
        *,
        db: Session = Depends(deps.get_db),
        listings_id: int,
        current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an listings.
    """
    listings = crud.listings.get(db=db, id=listings_id)
    if not listings:
        raise HTTPException(status_code=404, detail='Listings not found')
    listings = crud.listings.remove(db=db, id=listings_id)
    return listings
